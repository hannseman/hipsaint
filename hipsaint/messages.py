try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.request import ProxyHandler
    from urllib.request import build_opener
    from urllib.request import install_opener
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2 urllib2
    from urllib2 import urlopen, Request
    from urllib2 import ProxyHandler
    from urllib2 import build_opener
    from urllib2 import install_opener
    from urllib import urlencode
import logging
import socket
import json
from .options import COLORS
from .templates import templates

logging.basicConfig()
log = logging.getLogger(__name__)


class HipchatMessage(object):
    default_color = 'red'

    def __init__(self, msg_type, inputs, token, user, room_id, notify, api_host,
                 api_version, proxy=None, msg_format='html'):
        self.type = msg_type
        self.inputs = inputs
        self.inputs_list = [inp.strip() for inp in self.inputs.split('|')]
        self.token = token
        self.user = user
        self.room_id = room_id
        self.notify = notify
        self.host = api_host or 'api.hipchat.com'
        self.api_version = api_version
        self.urlv1 = 'https://{0}/v1/rooms/message'.format(self.host)
        self.urlv2 = 'https://{0}/v2/room/{1}/notification'.format(self.host, self.room_id)
        self.message_color = 'gray'
        self.message_format = msg_format
        self.proxy = proxy
        if self.proxy:
            self.setup_proxy()
        if str(self.api_version) != "2":
            self.url = self.urlv1
            self.deliver_payload = self.deliver_payload_v1
        else:
            self.url = self.urlv2
            self.deliver_payload = self.deliver_payload_v2

    def deliver_payload_v1(self, **kwargs):
        """
        Makes HTTP GET request to HipChat containing the message from nagios
        according to API Documentation https://www.hipchat.com/docs/api/method/rooms/message
        """
        message_body = self.render_message()
        message = {'room_id': self.room_id,
                   'from': self.user,
                   'message': message_body,
                   'color': self.message_color,
                   'notify': int(self.notify),
                   'auth_token': self.token}
        message.update(kwargs)
        message_params = urlencode(message)
        message_params = message_params.encode('utf-8')
        raw_response = urlopen(self.urlv1, message_params)
        response_data = json.load(raw_response)
        self.validate_response(response_data)
        return raw_response

    def deliver_payload_v2(self, **kwargs):
        """
        Makes HTTP POST request to HipChat containing the message from nagios
        according to API Documentation https://hipchat.corvisa.com/docs/apiv2/method/send_room_notification
        """
        message_body = self.render_message()
        message = {'message': message_body,
                   'color': self.message_color,
                   'notify': int(self.notify) > 0,
                   'message_format': self.message_format}
        message_params = json.dumps(message)
        message_params = message_params.encode('utf-8')
        headers = {'Authorization': 'Bearer {0}'.format(self.token),
                   'Content-Type': 'application/json'}
        request = Request(self.urlv2, message_params, headers)
        raw_response = urlopen(request)
        if raw_response.getcode() / 100 != 2:
            response_data = json.load(raw_response)
            self.validate_response(response_data)
        return raw_response

    def validate_response(self, response_data):
        """
        Check response for errors and log them
        """
        if 'error' in response_data:
            error_message = response_data['error'].get('message')
            error_type = response_data['error'].get('type')
            error_code = response_data['error'].get('code')
            log.error('%s - %s: %s', error_code, error_type, error_message)
        elif 'status' not in response_data:
            log.error('Unexpected response')

    def setup_proxy(self):
        """
        Setup http proxy
        """
        proxy = ProxyHandler({'https': self.proxy})
        opener = build_opener(proxy)
        install_opener(opener)

    def get_host_context(self):
        hostname, timestamp, ntype, hostaddress, state, hostoutput = self.inputs_list
        return {
            'hostname': hostname,
            'timestamp': timestamp,
            'ntype': ntype,
            'hostaddress': hostaddress,
            'state': state,
            'hostoutput': hostoutput
        }

    def get_service_context(self):
        servicedesc, hostalias, timestamp, ntype, hostaddress, state, serviceoutput = self.inputs_list
        return {
            'servicedesc': servicedesc,
            'hostalias': hostalias,
            'timestamp': timestamp,
            'ntype': ntype,
            'hostaddress': hostaddress,
            'state': state,
            'serviceoutput': serviceoutput
        }

    def render_message(self):
        """
        Unpacks Nagios inputs and renders the appropriate template depending
        on the notification type.
        """
        template_type = self.type
        if 'host' in template_type:
            template_context = self.get_host_context()
        elif 'service' in template_type:
            template_context = self.get_service_context()
        else:
            raise Exception('Invalid notification type')

        ntype = template_context['ntype']
        state = template_context['state']
        if ntype != 'PROBLEM':
            self.message_color = COLORS.get(ntype, self.default_color)
        else:
            self.message_color = COLORS.get(state, self.default_color)
        nagios_host = socket.gethostname()

        template_context.update(nagios_host=nagios_host)
        template = templates[template_type]
        return template.format(**template_context)
