#!/usr/bin/env python
from optparse import OptionParser
import hipsaint
from ..messages import HipchatMessage


def main():
    usage = "Usage: %prog [options] [action]..."

    parser = OptionParser(usage, version="%%prog v%s" % hipsaint.__version__)

    parser.add_option("-H", "--host",
                      dest="api_host",
                      default="api.hipchat.com",
                      help="HipChat Server to deliver message to (default: api.hipchat.com)")

    parser.add_option("-V", "--api_version",
                      dest="api_version",
                      default="1",
                      help="API version to use, either 1 or 2")

    parser.add_option("-r", "--room",
                      dest="room_id",
                      default="",
                      help="HipChat room id deliver message to")

    parser.add_option("-u", "--user",
                      dest="user",
                      default="Nagios",
                      help="Username to deliver message as, when using API version 1")

    parser.add_option("-t", "--token",
                      dest="token",
                      default="",
                      help="HipChat API token to use")

    parser.add_option("-i", "--inputs",
                      dest="inputs",
                      default="",
                      help="Input variables from Nagios separated by |")

    parser.add_option("-T", "--type",
                      dest="msg_type",
                      default="",
                      help="Mark if notification is from host group or service group, "
                           "host|service|short-host|short-service")

    parser.add_option("-n", "--notify",
                      action="store_true",
                      default=False,
                      dest="notify",
                      help="Whether or not this message should trigger a "
                           "notification for people in the room")

    parser.add_option("-f", "--format",
                      default="html",
                      dest="msg_format",
                      help="Determines how messages are rendered by HipChat."
                      "Valid values: html, text. Defaults to html.")

    parser.add_option("-p", "--proxy",
                      default="",
                      dest="proxy",
                      help="Specify a proxy in the form [user:passwd@]proxy.server:port.")

    ### Parse command line
    (options, args) = parser.parse_args()
    ### Validate required input
    if not options.token:
        parser.error('--token is required')
    if not options.inputs:
        parser.error('--inputs is required')
    if not options.room_id:
        parser.error('--room is required')
    if not options.msg_type:
        parser.error('--type is required')
    msg = HipchatMessage(**vars(options))
    msg.deliver_payload()


if __name__ == "__main__":
    main()
