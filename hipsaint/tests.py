from datetime import datetime
import unittest
from hipsaint.messages import HipchatMessage


class MessageTest(unittest.TestCase):

    def test_render_host(self):
        message_type = 'host'
        #"$HOSTNAME$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$HOSTSTATE$|$HOSTOUTPUT$" -n
        inputs = "hostname|%(longdatetime)s|%(notificationtype)s|127.0.0.1|%(hoststate)s|NAGIOS_OUTPUT"
        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'PROBLEM',
                               'hoststate': 'DOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'RECOVERY',
                               'hoststate': 'UP'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'green')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'UNREACHABLE',
                               'hoststate': 'UKNOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'ACKNOWLEDGEMENT',
                               'hoststate': 'DOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'purple')

    def test_render_service(self):
        message_type = 'service'
        #"$SERVICEDESC$|$HOSTALIAS$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$SERVICESTATE$|$SERVICEOUTPUT$"
        inputs = 'servicedesc|hostalias|%(longdatetime)s|%(notificationtype)s|127.0.0.1|%(servicestate)s|NAGIOS_OUTPUT'
        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'PROBLEM',
                               'servicestate': 'WARNING'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'yellow')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'PROBLEM',
                               'servicestate': 'CRITICAL'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'PROBLEM',
                               'servicestate': 'UNKNOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'gray')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'RECOVERY',
                               'servicestate': 'OK'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'green')

        msg_inputs = inputs % {'longdatetime': datetime.now(),
                               'notificationtype': 'ACKNOWLEDGEMENT',
                               'servicestate': 'CRITICAL'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'purple')
