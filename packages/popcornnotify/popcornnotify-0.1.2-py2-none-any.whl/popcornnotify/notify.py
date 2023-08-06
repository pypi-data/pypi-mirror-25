"""
PopcornNotify Python Client

An API for sending simple emails and text messages from your code
"""

import os
import requests
import threading


def notify(recipients=None, message=None, subject=None, api_key=None):
    try:
        notify_thread = threading.Thread(target=nonblocked_notify, args=(recipients, message, subject, api_key))
        notify_thread.start()

    except:
        # print "There was an issue with Popcorn Notify"
        pass


def nonblocked_notify(recipients=None, message=None, subject=None, api_key=None):
    if not api_key:
        api_key = os.environ['POPCORNNOTIFY_API_KEY']

    new_notify = PopcornNotify(
        recipients,
        message,
        subject=subject,
        api_key=api_key
    )


class PopcornNotify(object):

    def __init__(self, recipients, message, subject=None, api_key=None):

        self.api_key = api_key
        self.recipients = recipients
        self.message = message
        self.subject = subject

        is_debug = os.environ.get('POPCORNNOTIFY_SEND', 'true').lower()
        if is_debug in ['f', 'false', '0']:
            return

        self.post_to_server()

    def post_to_server(self):
        popcorn_notify_params = {
            'api_key': self.api_key,
            'recipients': self.recipients,
            'message': self.message,
            'subject': self.subject,
            # 'client': 'python',
            # 'version': notify.VERSION
        }

        url = 'https://popcornnotify.com/notify'
        r = requests.post(url, json=popcorn_notify_params)
        if r.status_code == 200:
            # print "Success!"
            pass
        else:
            pass
            # print "Popcorn Notify: There was an issue connecting to the Popcorn Notify Server"
            # print r.content  # this should be a good job or maybe an error
