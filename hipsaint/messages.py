try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2 urllib2
    from urllib2 import urlopen
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

    def __init__(self, msg_type, inputs, token, user, room_id, notify, api_host):
        self.type = msg_type
        self.inputs = inputs
        self.inputs_list = [inp.strip() for inp in self.inputs.split('|')]
        self.token = token
        self.user = user
        self.room_id = room_id
        self.notify = notify
        self.host = api_host or 'api.hipchat.com'
        self.url = 'https://{0}/v1/rooms/message'.format(self.host)
        self.message_color = 'gray'

    def deliver_payload(self, **kwargs):
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
        raw_response = urlopen(self.url, message_params)
        response_data = json.load(raw_response)
        if 'error' in response_data:
            error_message = response_data['error'].get('message')
            error_type = response_data['error'].get('type')
            error_code = response_data['error'].get('code')
            log.error('%s - %s: %s', error_code, error_type, error_message)
        elif not 'status' in response_data:
            log.error('Unexpected response')
        return raw_response

    def get_host_context(self):
        hostname, timestamp, ntype, hostaddress, state, hostoutput = self.inputs_list
        return {'hostname': hostname, 'timestamp': timestamp, 'ntype': ntype,
                'hostaddress': hostaddress, 'state': state, 'hostoutput': hostoutput}

    def get_service_context(self):
        servicedesc, hostalias, timestamp, ntype, hostaddress, state, serviceoutput = self.inputs_list
        return {'servicedesc': servicedesc, 'hostalias': hostalias, 'timestamp': timestamp,
                'ntype': ntype, 'hostaddress': hostaddress, 'state': state,
                'serviceoutput': serviceoutput}

    def render_message(self):
        """
        Unpacks Nagios inputs and renders the appropriate template depending
        on the notification type.
        """
        template_type = self.type
        if template_type in ('host', 'short-host'):
            template_context = self.get_host_context()
        elif template_type in ('service', 'short-service'):
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
