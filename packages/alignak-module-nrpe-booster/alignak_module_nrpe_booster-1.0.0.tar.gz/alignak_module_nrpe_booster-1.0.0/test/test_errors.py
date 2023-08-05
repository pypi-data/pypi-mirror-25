#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
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
"""
Test NRPE errors
"""

import re
import asyncore
import mock
import socket
import threading
import time

from alignak_test import AlignakTest
from alignak.check import Check

from test_simple import (
    NrpePollerTestMixin,
)

import alignak_module_nrpe_booster


class FakeNrpeServer(threading.Thread):
    def __init__(self, port=0):
        super(FakeNrpeServer, self).__init__()
        self.setDaemon(True)
        self.port = port
        self.cli_socks = []  # will retain the client socks here
        sock = self.sock = socket.socket()
        sock.settimeout(1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', port))
        if not port:
            self.port = sock.getsockname()[1]
        sock.listen(0)
        self.running = True
        self.start()

    def stop(self):
        self.running = False
        self.sock.close()

    def run(self):
        while self.running:
            try:
                sock, addr = self.sock.accept()
            except socket.error as err:
                pass
            else:
                # so that we won't block indefinitely in handle_connection
                # in case the client doesn't send anything :
                sock.settimeout(3)
                self.cli_socks.append(sock)
                self.handle_connection(sock)
                self.cli_socks.remove(sock)

    def handle_connection(self, sock):
        data = sock.recv(4096)
        # a valid nrpe response:
        data = b'\x00'*4 + b'\x00'*4 + b'\x00'*2 + 'OK'.encode() + b'\x00'*1022
        sock.send(data)
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        sock.close()


class Test_Errors(NrpePollerTestMixin, AlignakTest):

    def setUp(self):
        self.fake_server = FakeNrpeServer()

    def tearDown(self):
        self.fake_server.stop()
        self.fake_server.join()

    def test_bad_arguments(self):
        """ Bad arguments in the command
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        my_module = self._setup_nrpe()

        # We prepare a check in the to_queue
        command = ("$USER1$/check_nrpe -H 127.0.0.1 -P 12 -N -u -t 5 -c check_load3 -a 20")
        data = {
            'is_a': 'check',
            'status': 'queue',
            'command': command,
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        chk = Check(data)

        # Clear logs
        self.clear_logs()

        my_module.add_new_check(chk)

        my_module.launch_new_checks()

        self.assert_log_match('Could not parse a command: option -P not recognized', 0)

        # Check is already done
        self.assertEqual('done', chk.status)
        # Check has no connection
        self.assertIsNone(chk.con)
        self.assertEqual(2, chk.exit_status)
        self.assertEqual('Error: the host parameter is not correct.', chk.output)

    def test_no_host(self):
        """ No command required
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        fake_server = self.fake_server

        my_module = self._setup_nrpe()

        my_module.returns_queue = mock.MagicMock()

        # We prepare a check in the to_queue
        command = ("$USER1$/check_nrpe -p %s -n -u -t 5 -c check_load3 -a 20"
                   % fake_server.port)
        data = {
            'is_a': 'check',
            'status': 'queue',
            'command': command,
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        chk = Check(data)

        # GO
        my_module.add_new_check(chk)

        my_module.launch_new_checks()

        # Check is already done
        self.assertEqual('done', chk.status)
        # Check has no connection
        self.assertIsNone(chk.con)
        self.assertEqual(2, chk.exit_status)
        self.assertEqual('Error: the host parameter is not correct.', chk.output)

    def test_no_command(self):
        """ No command required
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        fake_server = self.fake_server

        my_module = self._setup_nrpe()

        my_module.returns_queue = mock.MagicMock()

        # We prepare a check in the to_queue
        command = ("$USER1$/check_nrpe -H 127.0.0.1 -p %s -n -u -t 5 -a 20"
                   % fake_server.port)
        data = {
            'is_a': 'check',
            'status': 'queue',
            'command': command,
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        chk = Check(data)

        # GO
        my_module.add_new_check(chk)

        self.assertFalse(fake_server.cli_socks,
                        'there should have no connected client to our fake server at this point')

        # Clear logs
        self.clear_logs()

        my_module.launch_new_checks()

        # Check is launched
        self.assertEqual('launched', chk.status)
        self.assertIsNotNone(chk.con)
        self.assertEqual(0, chk.retried)
        self.assertEqual('Sending request and waiting response...',
                         chk.con.message,
                         "what? chk=%s " % chk)

        # launch_new_checks() really launch a new check :
        # it creates the nrpe client and directly make it to connect
        # to the server.
        # To give a bit of time to our fake server thread to accept
        # the incoming connection from the client we actually need
        # to sleep just a bit of time:
        time.sleep(0.3)

        # if not chk.con.connected:
        #     asyncore.poll2(0)

        self.assertTrue(fake_server.cli_socks,
                        'the client should have connected to our fake server.\n'
                        '-> %s' % chk.con.message)

        # this makes sure for it to be fully processed.
        for _ in range(2):
            asyncore.poll2(0)
            time.sleep(0.1)

        my_module.manage_finished_checks()

        self.assertEqual(
            [], my_module.checks,
            "the check should have be moved out from the nrpe internal checks list")

        my_module.returns_queue.put.assert_called_once_with(chk)

        self.assertEqual(0, chk.exit_status)
        self.assertEqual(0, chk.retried)

    def test_retry_on_io_error(self):
        """

        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        fake_server = self.fake_server

        my_module = self._setup_nrpe()

        my_module.returns_queue = mock.MagicMock()

        # We prepare a check in the to_queue
        command = ("$USER1$/check_nrpe -H 127.0.0.1 -p %s -n -u -t 5 -c check_load3 -a 20"
                   % fake_server.port)
        data = {
            'is_a': 'check',
            'status': 'queue',
            'command': command,
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        chk = Check(data)

        # GO
        my_module.add_new_check(chk)

        self.assertFalse(fake_server.cli_socks,
                        'there should have no connected client to our fake server at this point')

        my_module.launch_new_checks()

        self.assertEqual('launched', chk.status)
        self.assertEqual(0, chk.retried)
        self.assertEqual('Sending request and waiting response...',
                         chk.con.message,
                         "what? chk=%s " % chk)

        # launch_new_checks() really launch a new check :
        # it creates the nrpe client and directly make it to connect
        # to the server.
        # To give a bit of time to our fake server thread to accept
        # the incoming connection from the client we actually need
        # to sleep just a bit of time:
        time.sleep(0.1)

        # if not chk.con.connected:
        #     asyncore.poll2(0)
        # if not chk.con.connected:
        #     asyncore.poll2(0)

        self.assertTrue(fake_server.cli_socks,
                        'the client should have connected to our fake server.\n'
                        '-> %s' % chk.con.message)

        # that should make the client to send us its request:
        asyncore.poll2(0)

        # give some time to the server thread to read it and
        # send its response:
        time.sleep(0.1)

        m = mock.MagicMock(side_effect=socket.error('boum'))
        chk.con.recv = m  # this is what will trigger the desired effect..

        self.assertEqual('Sending request and waiting response...',
                         chk.con.message)

        # that should make the client to have its recv() method called:
        asyncore.poll2(0)
        self.assertEqual("Error on read: boum", chk.con.message)

        save_con = chk.con  # we have to retain the con because its unset..

        # Clear logs
        self.clear_logs()

        # ..by manage_finished_checks :
        my_module.manage_finished_checks()

        self.assert_log_match(
            re.escape(
                '%s: Got an IO error (%s), retrying 1 more time.. (cur=%s)'
                % (chk.command, save_con.message, 0)
            ), 0
        )

        self.assertEqual('queue', chk.status)
        self.assertEqual(1, chk.retried, "the client has got the error we raised")

        # now the check is going to be relaunched:
        my_module.launch_new_checks()

        # this makes sure for it to be fully processed.
        for _ in range(2):
            asyncore.poll2(0)
            time.sleep(0.1)

        my_module.manage_finished_checks()

        self.assert_any_log_match(
            re.escape(
                '%s: Successfully retried check' % (chk.command)
            )
        )

        self.assertEqual(
            [], my_module.checks,
            "the check should have be moved out to the nrpe internal checks list")

        my_module.returns_queue.put.assert_called_once_with(chk)

        self.assertEqual(0, chk.exit_status)
        self.assertEqual(1, chk.retried)
