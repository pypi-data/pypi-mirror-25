Alignak checks package for the monitoring plugins
=================================================

*Checks pack for checking a lot of services: Dns, Http, Dhcp, ...*

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

This checks pack is based upon the check plugins of the `Monitoring Plugins Project <https://www.monitoring-plugins.org>`_.

This project is a bundle of around 50 standard plugins for monitoring applications. Some plugins allow to monitor local system metrics, others use various network protocols for remote checks.

*Our bundle was previously known as the “official” Nagios Plugins package.*
*The new name reflects both the success of the straightforward plugin interface originally invented*
*by the Nagios folks, and the popularity of our package, as the plugins are now used with various other monitoring products as well.*


Installation
------------

The pack configuration files are to be copied to the monitoring objects configuration directory. The most suitable location is the *arbiter/packs/* directory in the main alignak configuration directory.

**Note**: The main Alignak configuration directory is usually */usr/local/etc/alignak* or */etc/alignak* but it may depend upon your system and/or your installation.

The pack plugins (if any ...) are to be copied to the executable libraries directories.

**Note**: The Alignak librairies directory is usually */usr/local/var/libexec/alignak* but it may depend upon your system and/or your installation.

From PyPI
~~~~~~~~~
To install the package from PyPI:
::

   sudo pip install alignak-checks-monitoring


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-checks-monitoring
   cd alignak-checks-monitoring
   sudo pip install .

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*


Documentation
-------------

Configuration
~~~~~~~~~~~~~

To use this checks package, you must first install some external plugins. We recommend that you download and install the `Monitoring plugins`_.

.. _Monitoring plugins: https://www.monitoring-plugins.org/download.html

Check if it exists a binary package for your OS distribution rather than compiling and installing from source.
Else, the source installation procedure is explained `here`_.

.. _here: https://www.monitoring-plugins.org/doc/faq/installation.html

An abstract::

    $ wget https://www.monitoring-plugins.org/download/monitoring-plugins-2.X.tar.gz
    $ gzip -dc monitoring-plugins-2.X.tar.gz | tar -xf -
    $ cd monitoring-plugins-2.X
    $ ./configure --prefix /usr/local/libexec/monitoring-plugins
    $ make

    $ make install

    $ make install-root
    $ # This for plugins requiring setuid (check_icmp ...)

After compilation and installation, the plugins are installed in the */usr/local/libexec/monitoring-plugins/libexec* directory!

The */usr/local/etc/alignak/arbiter/packs/resource.d/monitoring.cfg* file defines a global macro
that contains the monitoring plugins installation path. If you do not install as default, edit
this file to update the path
::

    #-- Monitoring plugins installation directory
    $MONITORING_PLUGINS_DIR$=/usr/local/libexec/monitoring-plugins/libexec
    #--

Many information is available on the `project github repository`_, espacially in the REQUIREMENTS file.

.. _project github repository: https://github.com/monitoring-plugins/monitoring-plugins


Alignak configuration
~~~~~~~~~~~~~~~~~~~~~

You simply have to tag the concerned hosts with the template you are interested in.
::

    define host{
        use                     dns, ftp, http
        host_name               my_host
        address                 127.0.0.1
    }



Each template declares the associated services on the concerned host.
You can easily adapt the configuration defined in the ``templates.cfg``, ``services.cfg`` and ``commands.cfg`` files.


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-checks-monitoring/issues>`_ are the common way to raise an information.
