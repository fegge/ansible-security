#! /usr/bin/env python
import requests
import socket
import json
import os


WEBHOOK_CHANNEL = '#admin'
WEBHOOK_URL     = 'https://hooks.slack.com/services/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'


def _get_address(description):
    begin = description.index('from') + 5
    end = description.index('port') - 1
    return description[begin: end]


def _get_user(description):
    begin = description.index('for') + 4
    end = description.index('from') - 1
    return description[begin: end]

def _format_alert():
    hostname = socket.gethostname().title()
    fallback = 'Successful login to %s.' % hostname    
    try:
        user      = _get_user(os.environ['MONIT_DESCRIPTION'])
        address   = _get_address(os.environ['MONIT_DESCRIPTION'])
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
    data = {'channel': WEBHOOK_CHANNEL, 'attachments': attachments}
    return json.dumps(data)

if __name__ == '__main__':
    data = _format_alert()
    response = requests.post(WEBHOOK_URL, data=data)
    response.raise_for_status()
