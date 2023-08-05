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
Test the module
"""

import re
import time

from multiprocessing import Queue, Manager

from alignak_test import AlignakTest, time_hacker
from alignak.modulesmanager import ModulesManager
from alignak.objects.module import Module
from alignak.basemodule import BaseModule
from alignak.check import Check
from alignak.message import Message

import alignak_module_nrpe_booster


class TestModuleNrpeBooster(AlignakTest):
    """
    This class contains the tests for the module
    """

    def test_module_loading(self):
        """
        Alignak module loading

        :return:
        """
        self.print_header()
        self.setup_with_file('./cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)
        self.show_configuration_logs()

        # No arbiter modules created
        modules = [m.module_alias for m in self.arbiter.myself.modules]
        self.assertListEqual(modules, [])

        # The only existing broker module is logs declared in the configuration
        modules = [m.module_alias for m in self.brokers['broker-master'].modules]
        self.assertListEqual(modules, [])

        # No poller module
        modules = [m.module_alias for m in self.pollers['poller-master'].modules]
        self.assertListEqual(modules, ['nrpe-booster'])

        # No receiver module
        modules = [m.module_alias for m in self.receivers['receiver-master'].modules]
        self.assertListEqual(modules, [])

        # No reactionner module
        modules = [m.module_alias for m in self.reactionners['reactionner-master'].modules]
        self.assertListEqual(modules, [])

        # No scheduler modules
        modules = [m.module_alias for m in self.schedulers['scheduler-master'].modules]
        self.assertListEqual(modules, [])

    def test_module_manager(self):
        """
        Test if the module manager manages correctly all the modules
        :return:
        """
        self.print_header()
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        time_hacker.set_real_time()

        # Create an Alignak module
        mod = Module({
            'module_alias': 'nrpe-booster',
            'module_types': 'nrpe-booster',
            'python_name': 'alignak_module_nrpe_booster'
        })

        # Create the modules manager for a daemon type
        self.modulemanager = ModulesManager('poller', None)

        # Clear logs
        self.clear_logs()

        # Load and initialize the modules:
        #  - load python module
        #  - get module properties and instances
        self.modulemanager.load_and_init([mod])

        # Loading module logs
        self.assert_log_match(re.escape(
            "Importing Python module 'alignak_module_nrpe_booster' for nrpe-booster..."
        ), 0)
        self.assert_log_match(re.escape(
            "Module properties: {'daemons': ['poller'], 'phases': ['running'], "
            "'type': 'nrpe_poller', 'external': False, 'worker_capable': True}"
        ), 1)
        self.assert_log_match(re.escape(
            "Imported 'alignak_module_nrpe_booster' for nrpe-booster"
        ), 2)
        self.assert_log_match(re.escape(
            "Loaded Python module 'alignak_module_nrpe_booster' (nrpe-booster)"
        ), 3)
        self.assert_log_match(re.escape(
            "Give an instance of alignak_module_nrpe_booster for alias: nrpe-booster"
        ), 4)

        # Starting internal module logs
        self.assert_log_match("Trying to initialize module: nrpe-booster", 5)
        self.assert_log_match("Initialization of the NRPE poller module", 6)

        my_module = self.modulemanager.instances[0]

        # Get list of not external modules
        self.assertListEqual([my_module], self.modulemanager.get_internal_instances())
        for phase in ['configuration', 'late_configuration', 'retention']:
            self.assertListEqual([], self.modulemanager.get_internal_instances(phase))
        for phase in ['running']:
            self.assertListEqual([my_module], self.modulemanager.get_internal_instances(phase))

        # Get list of external modules
        self.assertListEqual([], self.modulemanager.get_external_instances())
        for phase in ['configuration', 'late_configuration', 'running', 'retention']:
            self.assertListEqual([], self.modulemanager.get_external_instances(phase))

        # Clear logs
        self.clear_logs()

        # Nothing special ...
        self.modulemanager.check_alive_instances()

        # And we clear all now
        self.modulemanager.stop_all()
        # Stopping module logs

        self.assert_log_match("Ending the NRPE poller module", 0)

    def test_module_start_default(self):
        """
        Test the module initialization function, no parameters, using default
        :return:
        """
        self.print_header()
        # Obliged to call to get a self.logger...
        self.setup_with_file('cfg/cfg_default.cfg')
        self.assertTrue(self.conf_is_correct)

        # -----
        # Default initialization
        # -----
        # Clear logs
        self.clear_logs()

        # Create an Alignak module
        mod = Module({
            'module_alias': 'nrpe-booster',
            'module_types': 'nrpe-booster',
            'python_name': 'alignak_module_nrpe_booster'
        })

        instance = alignak_module_nrpe_booster.get_instance(mod)
        self.assertIsInstance(instance, BaseModule)

        self.assert_log_match(
            re.escape("Give an instance of alignak_module_nrpe_booster for "
                      "alias: nrpe-booster"), 0)
