==========
 HipSaint
==========

Push your nagios notifications to HipChat using a simple command line tool.

.. image:: https://travis-ci.org/hannseman/hipsaint.png?branch=master
  :target: https://travis-ci.org/hannseman/hipsaint
   
.. image:: https://pypip.in/d/hipsaint/badge.png
  :target: https://pypi.python.org/pypi/hipsaint

Implements `HipChat message API`_.

.. _`hipchat message API`: https://www.hipchat.com/docs/api/method/rooms/message

Inspired by https://gist.github.com/2418848.

---------
 Install
---------

Through pip:

.. code-block:: bash

    pip install hipsaint


Or clone and simply run:

.. code-block:: bash

    python setup.py install

-------
 Usage in Nagios
-------

Assuming you use Nagios 3 add the following sections to commands.cfg with ``<TOKEN>`` and ``<ROOM_ID>`` specified and macros delimited by ``|``::

    define command {
        command_name    notify-host-by-hipchat
        command_line    hipsaint --token=<TOKEN> --room=<ROOM_ID> --type=host --inputs="$HOSTNAME$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$HOSTSTATE$|$HOSTOUTPUT$" -n
    }
    define command {
        command_name    notify-service-by-hipchat
        command_line    hipsaint --token=<TOKEN> --room=<ROOM_ID> --type=service --inputs="$SERVICEDESC$|$HOSTALIAS$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$SERVICESTATE$|$SERVICEOUTPUT$" -n
    }

To send less verbose messages to hipchat set the ``--type`` flag to either ``short-host`` or ``short-service``.

Additional commands is available through:

.. code-block:: bash

    hipsaint --help


Edit the Nagios contacts.cfg file by adding or editing an existing user and adding the notification commands created above::

    define contact {
            ....
            .....
            service_notification_commands   notify-service-by-hipchat
            host_notification_commands      notify-host-by-hipchat
            email   /dev/null
    }

-------
 Usage in Icinga 2
-------

To use Hipsaint in Icinga 2, you can create an additional config like this :

Create two scripts, one for hosts, one for services :

Don't forget to fill ``<TOKEN>`` and ``<ROOM_ID>``.

Hosts : /etc/icinga2/scripts/hipchat-host-notification.sh ::
    
    #!/bin/bash
    
    hipsaint --user=Icinga --token=<TOKEN> --room=<ROOM_ID> --type=host --inputs="$HOSTNAME|$LONGDATETIME|$NOTIFICATIONTYPE|$HOSTADDRESS|$HOSTSTATE|$HOSTOUTPUT" -n

Services : /etc/icinga2/scripts/hipchat-service-notification.sh ::

    #!/bin/bash

    hipsaint --user=Icinga --token=<TOKEN> --room=<ROOM_ID> --type=service --inputs="$SERVICEDESC|$HOSTALIAS|$LONGDATETIME|$NOTIFICATIONTYPE|$HOSTADDRESS|$SERVICESTATE|$SERVICEOUTPUT" -n

Then you need to tell Icinga to use those scripts :

Create a file called ``hipsaint.conf`` in your ``conf.d`` directory ::

    /**
     * Hipchat/Hipsaint script for Icinga2
     *
     * Only applied if host/service objects have
     * the custom attribute `sla` set to `24x7`.
     */

    object NotificationCommand "notify-host-by-hipchat" {
      import "plugin-notification-command"

      command = [ "/etc/icinga2/scripts/hipchat-host-notification.sh" ]

      env = {
        NOTIFICATIONTYPE = "$notification.type$"
        SERVICEDESC = "$service.name$"
        HOSTALIAS = "$host.display_name$"
        HOSTADDRESS = "$address$"
        SERVICESTATE = "$service.state$"
        LONGDATETIME = "$icinga.long_date_time$"
        SERVICEOUTPUT = "$service.output$"
      }
    }

    object NotificationCommand "notify-service-by-hipchat" {
      import "plugin-notification-command"

      command = [ "/etc/icinga2/scripts/hipchat-service-notification.sh" ]

      env = {
        NOTIFICATIONTYPE = "$notification.type$"
        SERVICEDESC = "$service.name$"
        HOSTALIAS = "$host.display_name$"
        HOSTADDRESS = "$address$"
        SERVICESTATE = "$service.state$"
        LONGDATETIME = "$icinga.long_date_time$"
        SERVICEOUTPUT = "$service.output$"
      }
    }

    apply Notification "hipchat-icingaadmin" to Host {
      command = "notify-host-by-hipchat"

      user_groups = [ "icingaadmins" ]

      assign where host.vars.sla == "24x7"
    }

    apply Notification "hipchat-icingaadmin" to Service {
      command = "notify-service-by-hipchat"

      user_groups = [ "icingaadmins" ]

      assign where service.vars.sla == "24x7"
    }

You want to customize this to your groups and users.
