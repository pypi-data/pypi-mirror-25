# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016: Alignak contrib team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak contrib projet.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#  Copyright (C) 2009-2012:
#     Gabes Jean, naparuba@gmail.com
#     Gerhard Lausser, Gerhard.Lausser@consol.de
#     Gregory Starck, g.starck@gmail.com
#     Hartmut Goebel, h.goebel@goebel-consult.de
#     Frédéric Mohier, frederic.mohier@gmail.com
#     David Durieux, d.durieux@siprossii.com
#
#  This file is part of Shinken.
#
#  Shinken is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shinken is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

"""
This module is an Alignak Broker module that collects the NSCA passive checks results, checks
their content and build an external command for the Alignak scheduler.
"""

import os
import time
import select
import socket
import struct
import random

import binascii

import logging

from alignak.basemodule import BaseModule
from alignak.external_command import ExternalCommand

logger = logging.getLogger('alignak.module')  # pylint: disable=C0103

# pylint: disable=C0103
properties = {
    'daemons': ['receiver'],
    'type': 'nsca',
    'external': True,
    'phases': ['running'],
    }


def decrypt_xor(data, key):
    """
    Decrypt the provided data using the WOR NSCA algorithm with the provided key
    :param data: data to decrypt
    :param key: encryption key
    :return:
    """
    keylen = len(key)
    crypted = [chr(ord(data[i]) ^ ord(key[i % keylen])) for i in xrange(len(data))]
    return ''.join(crypted)


def get_instance(mod_conf):
    """
    Return a module instance for the modules manager

    :param mod_conf: the module properties as defined globally in this file
    :return:
    """
    logger.info("Give an instance of %s for alias: %s", mod_conf.python_name, mod_conf.module_alias)

    return NSCACollector(mod_conf)


class NSCACollector(BaseModule):
    """
    NSCA collector module main class
    """
    def __init__(self, mod_conf):
        """
        Module initialization

        mod_conf is a dictionary that contains:
        - all the variables declared in the module configuration file
        - a 'properties' value that is the module properties as defined globally in this file

        :param mod_conf: module configuration file as a dictionary
        """
        BaseModule.__init__(self, mod_conf)

        # pylint: disable=global-statement
        global logger
        logger = logging.getLogger('alignak.module.%s' % self.alias)

        logger.debug("inner properties: %s", self.__dict__)
        logger.debug("received configuration: %s", mod_conf.__dict__)

        self.host = getattr(mod_conf, 'host', '127.0.0.1')
        if self.host == '*':
            self.host = ''
        self.port = int(getattr(mod_conf, 'port', '5667'))

        self.backlog = int(getattr(mod_conf, 'backlog', '10'))

        self.buffer_length = int(getattr(mod_conf, 'buffer_length', '4096'))
        self.payload_length = int(getattr(mod_conf, 'payload_length', '-1'))

        self.encryption_method = int(getattr(mod_conf, 'encryption_method', '0'))
        self.password = getattr(mod_conf, 'password', '')
        if self.password == "" and self.encryption_method != 0:
            logger.error("No password specified whereas an encryption method is defined")
            logger.warning("Setting password to 'dummy' to avoid crash!")
            self.password = "dummy"

        self.max_packet_age = min(int(getattr(mod_conf, 'max_packet_age', '30')), 900)
        self.check_future_packet = bool(getattr(mod_conf, 'check_future_packet', 'False'))

        self.output_decoding = getattr(mod_conf, 'output_decoding', 'UTF-8')

        self.rng = random.Random(self.password)

        logger.info(
            "configuration, allowed hosts : '%s'(%s), buffer length: %s, "
            "payload length: %s, encryption: %s, max packet age: %s, check future packet: %s, "
            "backlog: %d",
            self.host, self.port, self.buffer_length, self.payload_length,
            self.encryption_method, self.max_packet_age, self.check_future_packet, self.backlog)

    def send_init_packet(self, sock):
        """
        Build an init packet
         00-127: IV
         128-131: unix timestamp
        """
        iv = ''.join([chr(self.rng.randrange(256)) for i in xrange(128)])
        init_packet = struct.pack("!128sI", iv, int(time.time()))
        sock.send(init_packet)
        return iv

    def read_check_result(self, data, iv, payload_length):
        """
        Read the check result

        The !hhIIh64s128s512sh is the description of the packet.
        See Python doc for details. This is equivalent to the figure below

        00-01       Version
        02-03       Padding
        04-07       CRC32
        08-11       Timestamp
        12-13       Return Code
        14-77       Hostname
        78-205      Service name
        206-717     Plugin output (512 or 4096 bytes)
        718-719     Padding

        nsca.c (last version as of 2014-07)
        #define MAX_HOSTNAME_LENGTH         64
        #define MAX_DESCRIPTION_LENGTH      128
        #define MAX_PLUGINOUTPUT_LENGTH     4096

        #define OLD_PLUGINOUTPUT_LENGTH     512
        #define OLD_PACKET_LENGTH (( sizeof( data_packet) -
                                   ( MAX_PLUGINOUTPUT_LENGTH - OLD_PLUGINOUTPUT_LENGTH)))

        /* data packet containing service check results */
        typedef struct data_packet_struct{
            int16_t   packet_version;
            u_int32_t crc32_value;
            u_int32_t timestamp;
            int16_t   return_code;
            char      host_name[MAX_HOSTNAME_LENGTH];
            char      svc_description[MAX_DESCRIPTION_LENGTH];
            char      plugin_output[MAX_PLUGINOUTPUT_LENGTH];
        }data_packet;

        /* initialization packet containing IV and timestamp */
        typedef struct init_packet_struct{
            char      iv[TRANSMITTED_IV_SIZE];
            u_int32_t timestamp;
        }init_packet;
        """

        if self.encryption_method == 1:
            data = decrypt_xor(data, self.password)
            data = decrypt_xor(data, iv)
            logger.debug("Decrypted NSCA packet: %s", binascii.hexlify(data))

        try:
            # Python pack format for NSCA C structure
            # Depending on requested payload length
            unpack_format = "!hhIIh64s128s%ssh" % payload_length

            # version, pad1, crc32, timestamp, rc, hostname_dirty, service_dirty, output_dirty, pad2
            # are the name of unpacked structure elements
            (version, pad, crc32, timestamp, rc, hostname_dirty, service_dirty, output_dirty, _) = \
                struct.unpack(unpack_format, data)
            hostname = hostname_dirty.split("\0", 1)[0]
            service = service_dirty.split("\0", 1)[0]
            output = output_dirty.split("\0", 1)[0]
            output = output.decode(encoding=self.output_decoding, errors='ignore')

            # Output only the 256 first bytes of the output ... beware if some specific encoding
            # occurs after :)
            log_function = logger.debug
            if 'TEST_LOG_ACTIONS' in os.environ:
                log_function = logger.info

            log_function(
                "Decoded NSCA packet: host/service: %s/%s, timestamp: %d, output: %s",
                hostname, service, timestamp, output[:256]
            )
            return timestamp, rc, hostname, service, output
        except UnicodeDecodeError as e:
            # If initial decoding fails...
            logger.warning("Packet output decoding error: %s", str(e))
            logger.warning("Faulty NSCA packet content: %s", binascii.hexlify(data))
            return 0, 0, '', '', ''
        except Exception as e:
            logger.warning("Unable to decode NSCA packet: %s", str(e))
            logger.warning("Faulty NSCA packet content: %s", binascii.hexlify(data))
            return 0, 0, '', '', ''

    def post_command(self, timestamp, rc, hostname, service, output):
        """
        Send an external check result command to the receiver
        """
        if not service or service == 'host_check':
            extcmd = "[%lu] PROCESS_HOST_CHECK_RESULT;%s;%d;%s\n" % \
                (timestamp, hostname, rc, output)
        else:
            extcmd = "[%lu] PROCESS_SERVICE_CHECK_RESULT;%s;%s;%d;%s\n" % \
                (timestamp, hostname, service, rc, output)

        logger.debug(
            "external command: %s", extcmd
        )

        e = ExternalCommand(extcmd)
        self.from_q.put(e)

    def process_check_result(self, databuffer, iv):
        # 208 is the size of fixed received data ...
        # NSCA packets are 208+512 (720) or 208+4096 (4304)
        if not databuffer:
            logger.warning("Received an empty NSCA packet")
            return

        payload_length = len(databuffer) - 208
        if payload_length != 512 and payload_length != 4096:
            logger.warning(
                "Received packet with unusual payload length: %d.", payload_length
            )

        if self.payload_length != -1 and payload_length != self.payload_length:
            logger.warning("Dropping packet with incorrect payload length.")
            return

        (timestamp, rc, hostname, service, output) = self.read_check_result(
            databuffer, iv, payload_length
        )
        current_time = time.time()
        check_result_age = current_time - timestamp
        if timestamp > current_time and self.check_future_packet:
            logger.info("Dropping packet with future timestamp.")
        elif check_result_age > self.max_packet_age:
            logger.info(
                "Dropping packet with stale timestamp - packet was %s seconds old. "
                "Timestamp: %s" % (check_result_age, timestamp)
            )
        else:
            self.post_command(timestamp, rc, hostname, service, output)

    # Because the module is an "external" one, main loop of your process
    def main(self):
        """
        Main loop of the process

        This module is an "external" module
        :return:
        """
        # Set the OS process title
        self.set_proctitle(self.alias)
        self.set_exit_handler()

        logger.info("starting...")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(self.backlog)
        input = [server]
        databuffer = {}
        ivs = {}

        while not self.interrupted:
            # outputready and exceptready unused
            inputready, _, _ = select.select(input, [], [], 1)
            for s in inputready:
                if s == server:
                    # handle the server socket
                    try:
                        client, _ = server.accept()
                        iv = self.send_init_packet(client)
                        ivs[client] = iv
                        input.append(client)
                    except Exception as e:
                        logger.warning("Exception on socket connecting: %s", str(e))
                        continue
                else:
                    # handle all other sockets
                    try:
                        data = s.recv(self.buffer_length)
                        if s in databuffer:
                            databuffer[s] += data
                        else:
                            databuffer[s] = data
                    except Exception as e:
                        logger.warning("Exception on socket receiving: %s", str(e))
                        continue

                    if len(data) == 0:
                        self.process_check_result(databuffer[s], ivs[s])
                        try:
                            # Closed socket
                            del databuffer[s]
                            del ivs[s]
                        except:
                            pass
                        s.close()
                        input.remove(s)

        logger.info("stopping...")
        logger.info("stopped")
