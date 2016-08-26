#! /usr/bin/env python
import optparse
import requests
import socket
import json
import os


def _get_address(description):
    begin = description.index('from') + 5
    end = description.index('port') - 1
    return description[begin: end]


def _get_user(description):
    begin = description.index('for') + 4
    end = description.index('from') - 1
    return description[begin: end]


def _get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        "--webhook-url",
        dest="webhook_url",
        default=None,
        help="slack webhook url"
    )
    options, _ = parser.parse_args()
    if options.webhook_url is None:
        parser.error("mandatory argument missing")
    return options.webhook_url

def _format_alert():
    hostname = socket.gethostname().title()
    fallback = 'Successful login to %s.' % hostname    
    try:
        user = _get_user(os.environ['MONIT_DESCRIPTION'])
        address = _get_address(os.environ['MONIT_DESCRIPTION'])
        timestamp = os.environ['MONIT_DATE']
        value = '%s logged in as %s.\n%s' % (address, user, timestamp)
    except:
        value = 'New login detected.'    
    fields = [
        {
            'value': value,
            'short': False
        }
    ]
    attachments = [
        {
            'title': fallback,
            'fallback': fallback,
            'color': '#B5EAAA',
            'fields': fields
        }
    ]
    data = {'attachments': attachments}
    return json.dumps(data)

if __name__ == '__main__':
    data = _format_alert()
    webhook_url = _get_webhook_url()
    response = requests.post(webhook_url, data=data)
    response.raise_for_status()
