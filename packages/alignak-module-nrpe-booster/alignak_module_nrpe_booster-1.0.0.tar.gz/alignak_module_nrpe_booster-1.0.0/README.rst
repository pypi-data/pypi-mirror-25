Alignak NRPE booster Module
===========================

*Alignak NRPE booster module*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-nrpe-booster.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-module-nrpe-booster
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-nrpe-booster/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-module-nrpe-booster/develop
    :alt: Development code static analysis

.. image:: https://coveralls.io/repos/Alignak-monitoring-contrib/alignak-module-nrpe-booster/badge.svg?branch=develop
    :target: https://coveralls.io/r/Alignak-monitoring-contrib/alignak-module-nrpe-booster
    :alt: Development code tests coverage

.. image:: https://badge.fury.io/py/alignak_module_backend.svg
    :target: https://badge.fury.io/py/alignak-module-nrpe-booster
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Installation
------------

The installation of this module will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the modules (eg. *arbiter/modules*).

From PyPI
~~~~~~~~~
To install the module from PyPI:
::

   sudo pip install alignak-module-nrpe-booster


From source files
~~~~~~~~~~~~~~~~~
To install the module from the source files (for developing purpose):
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-module-nrpe-booster
   cd alignak-module-nrpe-booster
   sudo pip install . -e

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*


Short description
-----------------

This module allows Alignak Pollers to bypass the launch of the `check_nrpe` process. This allow to use NRPE checks without the need to install the Nagios NRPE plugin.

This module reads the check command and opens the connection by itself. It scales the use of NRPE for active monitoring of servers hosting NRPE agents.


Installation
------------

Requirements
~~~~~~~~~~~~
To use NRPE/SSL install `pyOpenssl` Python wrapper module with the OpenSSL library.


Configuration
-------------

Once installed, this module has its own configuration file in the */usr/local/etc/alignak/arbiter/modules* directory.
The default configuration file is *mod-nrpe-booster.cfg*. No configuration is necessary for this module.

Configure an Alignak poller to use this module:

    - edit your poller daemon configuration file
    - add the `module_alias` parameter value (`nrpe_booster`) to the `modules` parameter of the daemon

Tag the NRPE commands with the `module_type` parameter. This parameter must be the `module_alias` of the installed module::

    define command {
        command_name    check_nrpe
        command_line    $USER1$/check_nrpe -H $HOSTADRESS$ -c $ARG1$ -a $ARG2$
        module_type     nrpe-booster
    }



Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-module-nrpe-booster/issues>`_ are the common way to raise an information.
