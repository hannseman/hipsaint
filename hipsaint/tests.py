import unittest
import mock
from datetime import datetime
from hipsaint.messages import HipchatMessage


def setup_mock_request(mock_method, status_code, json):
    mock_response = mock.Mock()
    mock_response.json.return_value = json
    mock_response.status_code = status_code
    mock_method.return_value = mock_response


def mock_hipchat_ok_request(mock_method):
    data = {'status': 'sent'}
    return setup_mock_request(mock_method, 200, data)


def mock_hipchat_error_request(mock_method):
    data = {'error': {'message': 'some test error', 'type': 'Unauthorized', 'code': 401}}
    return setup_mock_request(mock_method, 401, data)


class MessageTest(unittest.TestCase):
    def setUp(self):
        #"$HOSTNAME$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$HOSTSTATE$|$HOSTOUTPUT$" -n
        self.host_inputs = 'hostname|%(longdatetime)s|%(notificationtype)s|127.0.0.1|%(hoststate)s|NAGIOS_OUTPUT'
        #"$SERVICEDESC$|$HOSTALIAS$|$LONGDATETIME$|$NOTIFICATIONTYPE$|$HOSTADDRESS$|$SERVICESTATE$|$SERVICEOUTPUT$"
        self.service_inputs = 'servicedesc|hostalias|%(longdatetime)s|%(notificationtype)s|127.0.0.1|%(servicestate)s|NAGIOS_OUTPUT'

    @mock.patch('requests.get')
    def test_ok_payload_delivery(self, mock_get):
        mock_hipchat_ok_request(mock_get)
        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'PROBLEM',
                                         'hoststate': 'DOWN'}
        problem_msg = HipchatMessage('host', msg_inputs, None, None, None, False)
        response = problem_msg.deliver_payload()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'sent')

    @mock.patch('requests.get')
    def test_error_payload_delivery(self, mock_get):
        mock_hipchat_error_request(mock_get)
        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'PROBLEM',
                                         'hoststate': 'DOWN'}
        problem_msg = HipchatMessage('host', msg_inputs, None, None, None, False)
        response = problem_msg.deliver_payload()
        self.assertEqual(response.status_code, 401)
        self.assertTrue('error' in response.json())

    def test_render_host(self):
        message_type = 'host'
        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'PROBLEM',
                                         'hoststate': 'DOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        # Test short host
        problem_msg = HipchatMessage('short-host', msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'RECOVERY',
                                         'hoststate': 'UP'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'green')

        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'UNREACHABLE',
                                         'hoststate': 'UKNOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = self.host_inputs % {'longdatetime': datetime.now(),
                                         'notificationtype': 'ACKNOWLEDGEMENT',
                                         'hoststate': 'DOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'purple')

    def test_render_service(self):
        message_type = 'service'
        msg_inputs = self.service_inputs % {'longdatetime': datetime.now(),
                                            'notificationtype': 'PROBLEM',
                                            'servicestate': 'WARNING'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'yellow')

        msg_inputs = self.service_inputs % {'longdatetime': datetime.now(),
                                            'notificationtype': 'PROBLEM',
                                            'servicestate': 'CRITICAL'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        # Test short service
        problem_msg = HipchatMessage('short-service', msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'red')

        msg_inputs = self.service_inputs % {'longdatetime': datetime.now(),
                                            'notificationtype': 'PROBLEM',
                                            'servicestate': 'UNKNOWN'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'gray')

        msg_inputs = self.service_inputs % {'longdatetime': datetime.now(),
                                            'notificationtype': 'RECOVERY',
                                            'servicestate': 'OK'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'green')

        msg_inputs = self.service_inputs % {'longdatetime': datetime.now(),
                                            'notificationtype': 'ACKNOWLEDGEMENT',
                                            'servicestate': 'CRITICAL'}
        problem_msg = HipchatMessage(message_type, msg_inputs, None, None, None, False)
        problem_msg.render_message()
        self.assertEqual(problem_msg.message_color, 'purple')
