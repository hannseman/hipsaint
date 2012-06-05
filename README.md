#HipSaint

Push your nagios notifications to HipChat using a simple command line tool.

Implements [HipChat message API](https://www.hipchat.com/docs/api/method/rooms/message).

Inspired by https://gist.github.com/2418848:

##Install

At the command line simply run:
~~~ sh
$ python setup.py install
~~~

##Documentation

Assuming you use Nagios 3 add the following sections to commands.cfg with &lt;TOKEN&gt; and &lt;ROOM_ID&gt; specified:

    define command {
        command_name    notify-host-by-hipchat
        command_line    hipsaint --token=<TOKEN> --room=<ROOM_ID> --type=host --inputs="$HOSTNAME$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$HOSTSTATE$|$HOSTOUTPUT$" -n
    }
    define command {
        command_name    notify-service-by-hipchat
        command_line    hipsaint --token=<TOKEN> --room=<ROOM_ID> --type=service --inputs="$SERVICEDESC$|$HOSTALIAS$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$SERVICESTATE$|$SERVICEOUTPUT$" -n
    }

Additional commands is available through:
~~~ sh
$ hipsaint --help
~~~

Edit the Nagios contacts.cfg file by adding or editing an existing user and adding the notification commands created above:

    define contact {
            ....
            .....
            service_notification_commands   notify-service-by-hipchat
            host_notification_commands      notify-host-by-hipchat
            email   /dev/null
    }
