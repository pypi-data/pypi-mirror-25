Alignak checks package for Mysql
================================

*Checks pack for monitoring mysql database server*

.. image:: https://badge.fury.io/py/alignak_checks_mysql.svg
    :target: https://badge.fury.io/py/alignak-checks-mysql
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Installation
------------

The installation of this checks pack will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the packs (eg. *arbiter/packs*).

From PyPI
~~~~~~~~~
To install the package from PyPI:
::

   sudo pip install alignak-checks-mysql


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-checks-mysql
   cd alignak-checks-linux-snmp
   sudo pip install .

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*



Documentation
-------------

This checks pack is using the some PERL plugins that are shipped with the checks pack. As such, some more installation and preparation are necessary;)


Configuration
~~~~~~~~~~~~~

**Note**: this pack embeds the ``check_mysql_health`` script from http://labs.consol.de/lang/en/nagios/check_mysql_health/.
The embedded version is built from the 2.2.2 version but you may install this script by yourself ...

We recommand that you download and install your own available from the web site.
An abstract::

    $ tar xvfz check_mysql_health-2.2.2
    $ cd check_mysql_health-2.2.2
    $ ./configure --prefix=/usr/local/var/libexec/alignak --with-nagios-user=alignak --with-nagios-group=alignak --with-mymodules-dir=/usr/local/var/libexec/alignak --with-mymodules-dyn-dir=/usr/local/var/libexec/alignak
    $ make

    $ make install

**Note**: replace */usr/local/var/libexec/alignak* according to your platform ...

After compilation and installation, the plugin is installed in the */usr/local/var/libexec/alignak* directory.

Edit the */usr/local/etc/alignak/arbiter/packs/resource.d/mysql.cfg* file and configure the credentials to access to the mysql server.
::

    #-- MySQL default credentials
    $MYSQLUSER$=root
    $MYSQLPASSWORD$=root


Install PERL dependencies for check_mysql_health plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You must install some PERL dependencies for the *check_mysql_health* script.

On some Linux distros, you can::

   su -
   apt-get install dbi-perl
   apt-get install dbd-mysql-perl

Or you can use the PERL *cpan* utility::

    cpan install DBI
    cpan install DBD::mysql

**Note**: you must have previously installed the mysql client for your operating system :)


Alignak configuration
~~~~~~~~~~~~~~~~~~~~~

You simply have to tag the concerned hosts with the template `mysql`.
::

    define host{
        use                     mysql
        host_name               my_server
        address                 127.0.0.1
    }

The main `mysql` template declares macros used to configure the launched checks. The default values of these macros listed hereunder can be overriden in each host configuration.
::

    _MYSQLUSER                      $MYSQLUSER$
    _MYSQLPASSWORD                  $MYSQLPASSWORD$

    _UPTIME_WARN		            10:
    _UPTIME_CRIT		             5:
    _CONNECTIONTIME_WARN             1
    _CONNECTIONTIME_CRIT             5
    _QUERYCACHEHITRATE_WARN         90:
    _QUERYCACHEHITRATE_CRIT         80:
    _THREADSCONNECTED_WARN          10
    _THREADSCONNECTED_CRIT          20
    _QCACHEHITRATE_WARN             90:
    _QCACHEHITRATE_CRIT             80:
    _QCACHELOWMEMPRUNES_WARN         1
    _QCACHELOWMEMPRUNES_CRIT        10
    _KEYCACHEHITRATE_WARN           99:
    _KEYCACHEHITRATE_CRIT           95:
    _BUFFERPOOLHITRATE_WARN         99:
    _BUFFERPOOLHITRATE_CRIT         95:
    _BUFFERPOOLWAITFREE_WARN         1
    _BUFFERPOOLWAITFREE_CRIT        10
    _LOGWAITS_WARN                   1
    _LOGWAITS_CRIT                  10
    _TABLECACHEHITRATE_WARN         99:
    _TABLECACHEHITRATE_CRIT         95:
    _TABLELOCKCONTENTION_WARN        1
    _TABLELOCKCONTENTION_CRIT        2
    _INDEXUSAGE_WARN                90:
    _INDEXUSAGE_CRIT                80:
    _TMPDISKTABLES_WARN             25
    _TMPDISKTABLES_CRIT             50
    _SLOWQUERIES_WARN               0.1
    _SLOWQUERIES_CRIT                1
    _LONGRUNNINGPROCS_WARN          10
    _LONGRUNNINGPROCS_CRIT          20
    _OPENFILES_WARN                 80
    _OPENFILES_CRIT                 95
    _THREADCACHEHITRATE_WARN        99:
    _THREADCACHEHITRATE_CRIT        95:


To set a specific value for an host, declare the same macro in the host definition file.
::

   define host{
        use                     mysql
        contact_groups          admins
        host_name               my_host
        address                 192.168.0.16

        # Specific values for this host
        _MYSQLUSER              root
        _MYSQLPASSWORD          root_pwd
   }


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-checks-mysql/issues>`_ are the common way to raise an information.
