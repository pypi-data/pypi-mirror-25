# -*- coding: utf-8 -*-
# pylint: disable=fixme
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
# Copyright (C) 2009-2012:
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.

"""
This module is an Alignak Poller module that allows to bypass the launch of the check_nrpe process.
"""

import re
import sys
import time
import getopt
import socket
import struct
import binascii
import asyncore
import logging
import signal
import Queue
import shlex

from alignak.basemodule import BaseModule

COMMUNICATION_ERRORS = (socket.error,)

# pylint: disable=wrong-import-position,invalid-name
try:
    import OpenSSL
except ImportError as openssl_import_error:
    OpenSSL = None
    SSLError = None
    SSLWantReadOrWrite = None
else:
    SSLError = OpenSSL.SSL.Error
    SSLWantReadOrWrite = (OpenSSL.SSL.WantReadError,
                          OpenSSL.SSL.WantWriteError)

    # consider SSLError's to also be a kind of communication error.
    COMMUNICATION_ERRORS += (SSLError,)
    # effectively, under SSL mode, any TCP reset or such failure
    # will be raised as such an instance of SSLError, which isn't
    # a subclass of IOError nor socket.error but we want to catch
    # both so to retry a check in such cases.
    # Look for 'retried' and 'readwrite_error' in the code..

logger = logging.getLogger('alignak.module')  # pylint: disable=C0103

# pylint: disable=C0103
properties = {
    'daemons': ['poller'],
    'type': 'nrpe_poller',
    'phases': ['running'],

    'external': False,

    # To be a real worker module, we must set this
    'worker_capable': True
}


def get_instance(mod_conf):
    """
    Return a module instance for the modules manager

    :param mod_conf: the module properties as defined globally in this file
    :return:
    """
    logger.info("Give an instance of %s for alias: %s", mod_conf.python_name, mod_conf.module_alias)

    return NrpePoller(mod_conf)


NRPE_DATA_PACKET_SIZE = 1034  # REALLY important .. !


# pylint: disable=too-few-public-methods
class NRPE(object):
    """
    NRPE protocol
    """
    def __init__(self, host, port, use_ssl, command):
        """
        Build a NRPE query packet
            00-01: NRPE protocol version
            02-03: packet type (01: query, 02: response)
            04-07: CRC32
            08-09: return code of the check if packet type is response
            10-1034: command (nul terminated)
            1035-1036: reserved

        :param host:
        :param port:
        :param use_ssl:
        :param command:
        """
        self.state = 'creation'
        self.host = host
        self.port = port
        self.use_sll = use_ssl
        self.rc = 3
        self.message = ''
        crc = 0

        # We pack it, then we compute CRC32 of this first query
        query = struct.pack(">2hih1024scc", 02, 01, crc, 0, command, 'N', 'D')
        crc = binascii.crc32(query)

        # we restart with the crc value this time
        # because python2.4 do not have pack_into.
        self.query = struct.pack(">2hih1024scc", 02, 01, crc, 0, command, 'N', 'D')

    def read(self, data):
        """
        Read a result and extract return code
        :param data:
        :return:
        """
        # TODO: Not sure to get all the data in one shot.
        # TODO we should buffer it until we get enough to unpack.

        if self.state == 'received':
            return self.rc, self.message

        self.state = 'received'
        # TODO: check crc

        try:
            response = struct.unpack(">2hih1024s", data)
        except struct.error as err:  # bad format...
            self.rc = 3
            self.message = ("Error : cannot unpack output ; "
                            "datalen=%s : err=%s" % (len(data), err))
        else:
            self.rc = response[3]
            # the output is padded with \x00 at the end so
            # we remove it.
            self.message = re.sub('\x00.*$', '', response[4])
            # crc_orig = response[2]

        return self.rc, self.message


class NRPEAsyncClient(asyncore.dispatcher, object):
    """
    NRPE client
    """
    # pylint: disable=too-many-arguments
    def __init__(self, host, port, use_ssl, timeout, unknown_on_timeout, msg):
        """

        :param host:
        :param port:
        :param use_ssl:
        :param timeout:
        :param unknown_on_timeout:
        :param msg:
        """
        asyncore.dispatcher.__init__(self)

        self.use_ssl = use_ssl
        self.start_time = time.time()
        self.timeout = timeout
        self._rc_on_timeout = 3 if unknown_on_timeout else 2
        self.readwrite_error = False  # there was an error at the tcp level..

        # Instantiate our nrpe helper
        self.nrpe = NRPE(host, port, self.use_ssl, msg)
        self.socket = None

        # And now we create a socket for our connection
        try:
            addrinfo = socket.getaddrinfo(host, port)[0]
        except socket.error as err:
            self.set_exit(2, "Cannot getaddrinfo: %s" % err)
            return

        self.create_socket(addrinfo[0], socket.SOCK_STREAM)

        if self.use_ssl:
            # The admin want a ssl connection,
            # but there is not openssl lib installed :(
            if OpenSSL is None:
                logger.warning("Python openssl lib is not installed! "
                               "Cannot use ssl, switching back to no-ssl mode; "
                               "original import error: %s",
                               openssl_import_error)
                self.use_ssl = False
            else:
                self.wrap_ssl()

        addr = (host, port)
        try:
            self.connect(addr)
        except socket.error as err:
            self.set_exit(2, "Cannot connect to %s: %s" % (addr, err))
        else:
            self.rc = 3
            self.message = 'Sending request and waiting response...'

    def wrap_ssl(self):
        """

        :return:
        """
        self.context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
        self.context.set_cipher_list('ADH')
        self._socket = self.socket  # keep the bare socket for later shutdown/close
        self.socket = OpenSSL.SSL.Connection(self.context, self.socket)
        self.set_accept_state()

    def close(self):
        """
        Close NRPE connection
        :return:
        """
        if self.socket is None:
            return
        if self.use_ssl:
            for _ in range(4):
                try:
                    if self.socket.shutdown():
                        break
                except SSLWantReadOrWrite:
                    pass  # just retry for now
                    # or:
                    # asyncore.poll2(0.5)
                    # but not sure we really need it as the SSL shutdown()
                    # should take care of it.
                except SSLError as err:
                    # on python2.7 I keep getting SSLError instance having no
                    # 'reason' nor 'library' attribute or any other detail.
                    # despite the docs telling the opposite:
                    # https://docs.python.org/2/library/ssl.html#ssl.SSLError
                    details = 'library=%s reason=%s : %s' % (
                        getattr(err, 'library', 'missing'),
                        getattr(err, 'reason', 'missing'),
                        err)
                    # output the error in debug mode for now.
                    logger.error('Error on SSL shutdown : %s', details)
                    logger.exception('Error on SSL shutdown : %s', err)
                    # keep retry.
            sock = self._socket
        else:
            sock = self.socket
        try:
            # Also always shutdown the underlying socket:
            # pylint: disable=too-many-function-args
            sock.shutdown(socket.SHUT_RDWR)
        except socket.error as err:
            logger.debug('socket.shutdown failed: %s', str(err))
        super(NRPEAsyncClient, self).close()
        self.socket = None

    def set_exit(self, rc, message):
        """
        Set NRPE request exit information
        :param rc: return code
        :param message: message
        :return:
        """
        self.close()
        self.rc = rc
        self.message = message
        self.execution_time = time.time() - self.start_time
        self.nrpe.state = 'received'

    def look_for_timeout(self):
        """
        Check if we are in timeout. If so, just bailout and set the correct return code
        from timeout case
        :return:
        """
        now = time.time()
        if now - self.start_time > self.timeout:
            message = ('Error: connection timeout after %d seconds'
                       % self.timeout)
            self.set_exit(self._rc_on_timeout, message)

    def handle_read(self):
        """
        We got a read from the socket and keep receiving until it has finished.
        Maybe it's just a SSL handshake continuation, if so we continue
        and wait for handshake finish
        :return:
        """
        if self.is_done():
            return
        try:
            self._handle_read()
        except COMMUNICATION_ERRORS as err:
            self.readwrite_error = True
            self.set_exit(2, "Error on read: %s" % err)

    def _handle_read(self):
        """
        Read received data
        :return:
        """
        try:
            buf = self.recv(NRPE_DATA_PACKET_SIZE)
        except SSLWantReadOrWrite:
            # if we are in ssl, there can be a handshake
            # problem: we can't talk until we finished it.
            try:
                self.socket.do_handshake()
            except SSLWantReadOrWrite:
                pass
            return
        else:
            # Maybe we got nothing from the server (it refused our IP,
            # or our arguments...)
            if buf:
                rc, message = self.nrpe.read(buf)
            else:
                rc = 2
                message = "Error: Empty response from the NRPE server. Are we blacklisted ?"

        self.set_exit(rc, message)

    def writable(self):
        """
        Did we finished our job?
        :return:
        """
        return not self.is_done() and self.nrpe.query

    def handle_write(self):
        """
        We can write to the socket. If we are in the ssl handshake phase we just continue
        and return. If we finished, we can write our query
        :return:
        """
        try:
            self._handle_write()
        except COMMUNICATION_ERRORS as err:
            self.readwrite_error = True
            self.set_exit(2, 'Error on write: %s' % err)

    def _handle_write(self):
        """
        Write data
        :return:
        """
        try:
            sent = self.send(self.nrpe.query)
        except SSLWantReadOrWrite:
            # SSL write/send can require a read ! yes ;)
            try:
                self.socket.do_handshake()
            except SSLWantReadOrWrite:
                # still not finished, we continue
                pass
        else:
            # Maybe we did not sent all our query so we bufferize it
            self.nrpe.query = self.nrpe.query[sent:]

    def is_done(self):
        """
        NRPE check finished
        :return:
        """
        return self.nrpe.state == 'received'

    def handle_error(self):
        """
        Handle an error
        :return:
        """
        _, err, _ = sys.exc_info()
        self.set_exit(2, "Error: %s" % str(err))


def parse_args(cmd_args):
    """
    Parse check_nrpe arguments
    :param cmd_args:
    :return:
    """
    # Default params
    host = None
    command = None
    port = 5666
    unknown_on_timeout = False
    timeout = 10
    use_ssl = True
    add_args = []

    # Manage the options
    # NRPE Plugin for Nagios
    # Copyright (c) 1999-2008 Ethan Galstad (nagios@nagios.org)
    # Version: 2.15
    # Last Modified: 09-06-2013
    # License: GPL v2 with exemptions (-l for more info)

    # Usage: check_nrpe -H <host> [ -b <bindaddr> ]
    #                   [-4] [-6] [-n] [-u]
    #                   [-p <port>] [-t <timeout>]
    #                   [-c <command>] [-a <arglist...>]

    # Options:
    #  -n         = Do no use SSL
    #  -u         = Make socket timeouts return an UNKNOWN state instead of CRITICAL
    #  <host>     = The address of the host running the NRPE daemon
    #  <bindaddr> = bind to local address
    #  -4         = user ipv4 only
    #  -6         = user ipv6 only
    #  [port]     = The port on which the daemon is running (default=5666)
    #  [timeout]  = Number of seconds before connection times out (default=10)
    #  [command]  = The name of the command that the remote daemon should run
    #  [arglist]  = Optional arguments that should be passed to the command.  Multiple
    #               arguments should be separated by a space.  If provided, this must be
    #               the last option supplied on the command line.

    # Note:
    # This plugin requires that you have the NRPE daemon running on the remote host.
    # You must also have configured the daemon to associate a specific plugin command
    # with the [command] option you are specifying here.  Upon receipt of the
    # [command] argument, the NRPE daemon will run the appropriate plugin command and
    # send the plugin output and return code back to *this* plugin.  This allows you
    # to execute plugins on remote hosts and 'fake' the results to make Nagios think
    # the plugin is being run locally.

    logger.debug("Received arguments: %s", cmd_args)
    try:
        opts, args = getopt.getopt(cmd_args, "H::p::nut::c::a::", [])
    except getopt.GetoptError as err:
        # If we got problem, bail out - say host is None
        logger.exception("Could not parse a command: %s", err)
        return None, port, unknown_on_timeout, command, timeout, use_ssl, add_args

    logger.debug("Parsed arguments: opts = %s, args = %s", opts, args)
    try:
        for o, a in opts:
            if o == "-H":
                host = a
            elif o == "-p":
                port = int(a)
            elif o == "-c":
                command = a
            elif o == '-t':
                timeout = int(a)
            elif o == '-u':
                unknown_on_timeout = True
            elif o == '-n':
                use_ssl = False
            elif o == '-a':
                # Here we got a, btu also all 'args'
                add_args.append(a)
                add_args.extend(args)
    except ValueError as err:
        # If we got problem, bail out - say host is None
        logger.error("Could not parse command parameters: %s", cmd_args)
        logger.error("Check the module and command configuration (macros, ...)")
        return None, port, unknown_on_timeout, command, timeout, use_ssl, add_args

    return host, port, unknown_on_timeout, command, timeout, use_ssl, add_args


class NrpePoller(BaseModule):
    """
    NRPE Poller module main class
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
        logger.debug("loaded into: %s", self.loaded_into)

        self.checks = []

        self.returns_queue = None
        self.s = None
        self.t_each_loop = None

        self.i_am_dying = False

    def init(self):
        """
        Called by the poller to initialize the module
        :return: True to inform ModuleManager of a correct initialization
        """
        logger.info("Initialization of the NRPE poller module")
        self.i_am_dying = False

        return True

    def quit(self):
        """
        Called by the poller to exit the module
        :return: None
        """
        logger.info("Ending the NRPE poller module")

    def do_loop_turn(self):
        pass

    def add_new_check(self, check):
        """
        Add a new check to execute
        :param check: alignak.Check
        :return:
        """
        check.retried = 0
        logger.debug("Got a new check: %s", check.__dict__)
        self.checks.append(check)

    def get_new_checks(self):
        """

        :return:
        """
        while True:
            try:
                msg = self.s.get(block=False)
            except Queue.Empty:
                return
            if msg is not None:
                check = msg.get_data()
                self.add_new_check(check)

    def launch_new_checks(self):
        """
        Launch the new received checks
        :return:
        """
        for check in self.checks:
            now = time.time()
            if check.status == 'queue':
                check.con = None

                # Ok we launch it
                check.status = 'launched'
                check.check_time = now

                # We want the args of the commands so we parse it like a shell
                # shlex want str only
                clean_command = shlex.split(check.command.encode('utf8', 'ignore'))

                # If the command seems good
                if len(clean_command) > 1:
                    # we do not want the first member, check_nrpe thing
                    args = parse_args(clean_command[1:])
                    (host, port, unknown_on_timeout, command, timeout, use_ssl, add_args) = args
                    logger.debug("Parsed arguments: %s / %s / %s / %s / %s / %s / %s",
                                 host, port, unknown_on_timeout, command, timeout, use_ssl,
                                 add_args)
                else:
                    # Set an error so we will quit this check
                    command = None

                # If we do not have the good args, we bail out for this check
                if host is None:
                    check.status = 'done'
                    check.exit_status = 2
                    check.get_outputs('Error: the host parameter is not correct.', 8012)
                    check.execution_time = 0
                    continue

                # if no command is specified, check_nrpe
                # sends _NRPE_CHECK as default command.
                if command is None:
                    command = '_NRPE_CHECK'

                # Ok we are good, we go on
                total_args = [command]
                total_args.extend(add_args)
                cmd = r'!'.join(total_args)
                logger.info("Launch NRPE check: %s", cmd)
                check.con = NRPEAsyncClient(host, port, use_ssl, timeout, unknown_on_timeout, cmd)

    def manage_finished_checks(self):
        """
        Check the status of the checks
        :return:
        """
        to_del = []

        # First look for checks in timeout
        for check in self.checks:
            if check.status == 'launched':
                check.con.look_for_timeout()

        # Now we look for finished checks
        for check in self.checks:
            # First manage check in error, bad formed
            if check.status == 'done':
                to_del.append(check)
                self.returns_queue.put(check)

            # Then we check for good checks
            elif check.status == 'launched' and check.con.is_done():
                con = check.con
                # unlink our object from the original check,
                # this might be necessary to allow the check to be again
                # serializable..
                del check.con
                if con.readwrite_error and check.retried < 2:
                    logger.warning('%s: Got an IO error (%s), retrying 1 more time.. (cur=%s)',
                                   check.command, con.message, check.retried)
                    check.retried += 1
                    check.status = 'queue'
                    continue

                if check.retried:
                    logger.info('%s: Successfully retried check :)', check.command)

                check.status = 'done'
                check.exit_status = con.rc
                check.get_outputs(con.message, 8012)
                check.execution_time = con.execution_time

                # and set this check for deleting
                # and try to send it
                to_del.append(check)
                self.returns_queue.put(check)

        # And delete finished checks
        for chk in to_del:
            self.checks.remove(chk)

    # Wrapper function for do_work in order to catch potential exceptions
    def work(self, s, returns_queue, c):
        """
        Wrapper function for work in order to catch the exception
        to see the real work, look at do_work
        """
        try:
            self.do_work(s, returns_queue, c)
        except Exception as err:
            logger.exception("Got an unhandled exception: %s", err)
            # Ok I die now
            raise

    def do_work(self, s, returns_queue, c):
        """

        :param s: global queue
        :param returns_queue: queue of our manager
        :param c: control queue for the worker
        :return:
        """
        logger.debug("Module worker started!")
        # restore default signal handler for the workers:
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        self.returns_queue = returns_queue
        self.s = s
        self.t_each_loop = time.time()

        while True:

            # We check if all new things in connections
            # NB : using poll2 instead of poll (poll1 is with select
            # call that is limited to 1024 connexions, poll2 is ... poll).
            asyncore.poll2(1)

            # If we are dying (big problem!) we do not
            # take new jobs, we just finished the current one
            if not self.i_am_dying:
                # REF: doc/shinken-action-queues.png (3)
                self.get_new_checks()
                # REF: doc/shinken-action-queues.png (4)
                self.launch_new_checks()

            # REF: doc/shinken-action-queues.png (5)
            self.manage_finished_checks()

            # Now get order from master, if any..
            try:
                msg = c.get(block=False)
            except Queue.Empty:
                pass
            else:
                logger.debug("Got message: %s", msg.__dict__)
                if msg.get_type() == 'Die':
                    logger.info("[NRPEPoller] Dad says we should die...")
                    break
