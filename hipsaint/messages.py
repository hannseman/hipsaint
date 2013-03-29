import logging
import requests
import socket
from os import path
from jinja2.loaders import FileSystemLoader
from jinja2 import Environment
from hipsaint.options import COLORS

logging.basicConfig()
log = logging.getLogger(__name__)


class HipchatMessage(object):
    url = "https://api.hipchat.com/v1/rooms/message"
    default_color = 'red'

    def __init__(self, type, inputs, token, user, room_id, notify, **kwargs):
        self.type = type
        self.inputs = inputs
        self.token = token
        self.user = user
        self.room_id = room_id
        self.notify = notify

    def deliver_payload(self, **kwargs):
        """ Makes HTTP GET request to HipChat containing the message from nagios
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
        raw_response = requests.get(self.url, params=message)
        response_data = raw_response.json()
        if 'error' in response_data:
            error_message = response_data['error'].get('message')
            error_type = response_data['error'].get('type')
            error_code = response_data['error'].get('code')
            log.error('%s - %s: %s', error_code, error_type, error_message)
        elif not 'status' in response_data:
            log.error('Unexpected response')
        return raw_response

    def render_message(self):
        """ Unpacks Nagios inputs and renders the appropriate template depending
            on the notification type.
        """
        template_type = self.type
        if template_type == 'host' or template_type == 'short-host':
            hostname, timestamp, ntype, hostaddress, state, hostoutput = self.inputs.split('|')
        elif template_type == 'service' or template_type == 'short-service':
            servicedesc, hostalias, timestamp, ntype, hostaddress, state, serviceoutput = self.inputs.split('|')
        else:
            raise Exception('Invalid notification type')

        if ntype != 'PROBLEM':
            self.message_color = COLORS.get(ntype, self.default_color)
        else:
            self.message_color = COLORS.get(state, self.default_color)
        nagios_host = socket.gethostname().split('.')[0]

        template_path = path.realpath(path.join(path.dirname(__file__), 'templates'))
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('%s.html' % template_type)
        context = locals()
        context.pop('self')
        return template.render(**context)
