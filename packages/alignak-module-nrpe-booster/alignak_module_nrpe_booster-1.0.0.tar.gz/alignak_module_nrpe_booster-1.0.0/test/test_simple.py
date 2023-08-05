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

import os
import time
import logging

from multiprocessing import Queue, Manager
from alignak_test import AlignakTest
from alignak.check import Check

try:
    import unittest2 as unittest
except ImportError:
    import unittest


from alignak.modulesmanager import ModulesManager
from alignak.objects.module import Module
from alignak.message import Message

import alignak_module_nrpe_booster

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



class NrpePollerTestMixin(object):

    def setUp(self):
        super(NrpePollerTestMixin, self).setUp()
        logger.setLevel(logging.DEBUG)

    def _setup_nrpe(self):
        # Create an Alignak module
        mod = Module({
            'module_alias': 'nrpe-booster',
            'module_types': 'nrpe-booster',
            'python_name': 'alignak_module_nrpe_booster'
        })

        # Create the modules manager for a daemon type
        self.modulemanager = ModulesManager('poller', None)
        # Load and initialize the modules
        self.modulemanager.load_and_init([mod])
        my_module = self.modulemanager.instances[0]
        return my_module


@unittest.skipIf(os.name == 'nt', "NRPE poller do not run with Windows")
class TestNrpePoller(NrpePollerTestMixin, AlignakTest):
    def test_nrpe_poller(self):
        """

        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        my_module = self._setup_nrpe()

        manager = Manager()
        to_queue = manager.Queue()
        from_queue = manager.Queue()
        control_queue = Queue()

        # We prepare a check in the to_queue
        data = {
            'is_a': 'check',
            'status': 'queue',
            'command': "$USER1$/check_nrpe -H localhost33  -n -u -t 5 -c check_load3 -a 20",
            'timeout': 10,
            'poller_tag': None,
            't_to_go': time.time(),
            'ref': None,
        }
        c = Check(data)

        msg = Message(_type='Do', data=c)
        to_queue.put(msg)

        # The worker will read a message by loop. We want it to do 2 loops,
        # so we fake a message, and the second message is a real exit one
        msg1 = Message(_type='Continue')
        msg2 = Message(_type='Die')
        control_queue.put(msg1)
        for _ in xrange(1, 2):
            control_queue.put(msg1)
        control_queue.put(msg2)

        # Call module working ...
        my_module.work(to_queue, from_queue, control_queue)

        chk = from_queue.get()
        self.assertEqual('done', chk.status)
        self.assertEqual(2, chk.exit_status)
