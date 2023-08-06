Alignak checks package for NRPE checked hosts/services
======================================================

*Checks pack for monitoring Unix/Linux or Windows hosts with NRPE active checks*


.. image:: https://badge.fury.io/py/alignak_checks_nrpe.svg
    :target: https://badge.fury.io/py/alignak-checks-nrpe
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3


**Note:** *this check pack is only an example for checking linux / windows hosts using the Nagios NRPE commands. Please feel free to comment or suggest improvements :)*


Installation
------------

The installation of this checks pack will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the packs (eg. *arbiter/packs*).

From PyPI
~~~~~~~~~
To install the package from PyPI:
::

   sudo pip install alignak-checks-nrpe


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-checks-nrpe
   cd alignak-checks-nrpe
   sudo pip install .

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*

Documentation
-------------

Configuration
~~~~~~~~~~~~~

This checks pack is using the `check_nrpe` Nagios plugin that must be installed on the Alignak server running your poller daemon.

For Unix (FreeBSD), you can simply install the NRPE plugin:
::

   # Simple NRPE
   pkg install nrpe

   # NRPE with SSL
   pkg install nrpe-ssl

   # Take care to copy/rename the check_nrpe2 to check_nrpe if needed! Else, replace the check_nrpe
   # command with check_nrpe2

For Linux distros, install the Nagios ``check_nrpe`` plugin from your system repository:
::

   # Install local NRPE plugin
   sudo apt-get install nagios-nrpe-plugin
   # Note: This may install all the Nagios stuff on your machine...


After installation, the plugins are commonly installed in the */usr/local/libexec/nagios* directory.

The */usr/local/etc/alignak/arbiter/packs/resource.d/nrpe.cfg* file defines a global macro
that contains the NRPE check plugin installation path. You must edit this file to update the default path that is defined to the alignak ``$NAGIOSPLUGINSDIR$`` (defined in alignak default configuration).
::

    #-- NRPE check plugin installation directory
    # Default is to use the Alignak plugins directory
    $NRPE_PLUGINS_DIR$=$NAGIOSPLUGINSDIR$
    #--

**Note:** the default value for ``$NAGIOSPLUGINSDIR$`` is set as */usr/lib/nagios/plugins* which is the common installation directory used by the Nagios plugins.


Prepare Unix/Linux monitored hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some operations are necessary on the monitored hosts if NRPE remote access is not yet activated.
::
   # Install local NRPE server
   su -
   apt-get update
   apt-get install nagios-nrpe-server
   apt-get install nagios-plugins

   # Allow Alignak as a remote host
   vi /etc/nagios/nrpe.cfg
   =>
      allowed_hosts = X.X.X.X

   # Restart NRPE daemon
   /etc/init.d/nagios-nrpe-server start

Test remote access with the plugins files:
::

   /usr/lib/nagios/plugins/check_nrpe -H 127.0.0.1 -t 9 -u -c check_load

**Note**: This configuration is the default Nagios NRPE daemon configuration. As such it does not allow to define arguments in the NRPE commands and, as of it, the warning / critical threshold are defined on the server side.


Prepare Windows monitored hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some operations are necessary on the Windows monitored hosts if NSClient++ is not yet installed and running.

Install and configure NSClient++ to allow remote NRPE checks. The example below is an NSClient Ini configuration file that allows to use the NRPE server.

::

    # -----------------------------------------------------------------------------
    # c:\Program Files\NSClient++\nsclient.ini
    # -----------------------------------------------------------------------------

    [/modules]
    CheckExternalScripts = 1
    CheckEventLog = 1
    CheckDisk = 1
    CheckSystem = 1
    NRPEServer = 1

    [/settings/default]
    ; Alignak server Ip address
    allowed hosts = address = 192.168.15.1

    [/settings/external scripts/alias]
    alias_cpu = checkCPU warn=80 crit=90 time=5m time=1m time=30s
    alias_cpu_ex = checkCPU warn=$ARG1$ crit=$ARG2$ time=5m time=1m time=30s
    alias_disk = CheckDriveSize MinWarn=10% MinCrit=5% CheckAll FilterType=FIXED
    alias_disk_loose = CheckDriveSize MinWarn=10% MinCrit=5% CheckAll FilterType=FIXED ignore-unreadable
    alias_event_log = CheckEventLog file=application file=system MaxWarn=1 MaxCrit=1 "filter=generated gt -2d AND severity NOT IN ('success', 'informational') AND source != 'SideBySide'" truncate=800 unique descriptions "syntax=%severity%: %source%: %message% (%count%)"
    alias_file_age = checkFile2 filter=out "file=$ARG1$" filter-written=>1d MaxWarn=1 MaxCrit=1 "syntax=%filename% %write%"
    alias_file_size = CheckFiles "filter=size > $ARG2$" "path=$ARG1$" MaxWarn=1 MaxCrit=1 "syntax=%filename% %size%" max-dir-depth=10
    alias_mem = checkMem MaxWarn=80% MaxCrit=90% ShowAll=long type=physical type=virtual type=paged type=page
    alias_process = checkProcState "$ARG1$=started"
    alias_process_count = checkProcState MaxWarnCount=$ARG2$ MaxCritCount=$ARG3$ "$ARG1$=started"
    alias_process_hung = checkProcState MaxWarnCount=1 MaxCritCount=1 "$ARG1$=hung"
    alias_process_stopped = checkProcState "$ARG1$=stopped"
    alias_sched_all = CheckTaskSched "filter=exit_code ne 0" "syntax=%title%: %exit_code%" warn=>0
    alias_sched_long = CheckTaskSched "filter=status = 'running' AND most_recent_run_time < -$ARG1$" "syntax=%title% (%most_recent_run_time%)" warn=>0
    alias_sched_task = CheckTaskSched "filter=title eq '$ARG1$' AND exit_code ne 0" "syntax=%title% (%most_recent_run_time%)" warn=>0
    alias_service = checkServiceState CheckAll
    alias_service_ex = checkServiceState CheckAll "exclude=Net Driver HPZ12" "exclude=Pml Driver HPZ12" exclude=stisvc
    alias_up = checkUpTime MinWarn=1d MinWarn=1h
    alias_updates = check_updates -warning 0 -critical 0
    alias_volumes = CheckDriveSize MinWarn=10% MinCrit=5% CheckAll=volumes FilterType=FIXED
    alias_volumes_loose = CheckDriveSize MinWarn=10% MinCrit=5% CheckAll=volumes FilterType=FIXED ignore-unreadable
    default =

    [/settings/NRPE/server]
    ; COMMAND ARGUMENT PROCESSING - This option determines whether or not the we will allow clients to specify arguments to commands that are executed.
    allow arguments = true

    allow nasty characters = false
    insecure = true
    encoding = utf8

Test remote access with the plugins files:
::

   /usr/lib/nagios/plugins/check_nrpe -H 127.0.0.1 -t 9 -u -c check_load



Alignak configuration
~~~~~~~~~~~~~~~~~~~~~

For a Linux monitored host, you simply have to tag the concerned host with the template ``linux-nrpe``.
::

    define host{
        use                     linux-nrpe
        host_name               linux_nrpe
        address                 127.0.0.1
    }




For a Windows monitored host, you simply have to tag the concerned host with the template ``windows-nrpe``.
::

    define host{
        use                     windows-nrpe
        host_name               windows_nrpe
        address                 127.0.0.1
    }





Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-checks-nrpe/issues>`_ are the common way to raise an information.
