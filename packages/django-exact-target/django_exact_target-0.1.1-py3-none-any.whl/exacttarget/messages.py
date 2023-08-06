from raven.contrib.django.raven_compat.models import client as raven_client
import requests
from . import token, exceptions


class TriggeredSend(object):
    url_base = 'https://www.exacttargetapis.com/messaging/v1/messageDefinitionSends'

    def __init__(self, external_key):
        self.external_key = external_key
        self.token = token.CachedTokenGenerator()


    def dispatch(self, email, attrs):
        url = '%s/key:%s/send' % (self.url_base, self.external_key)
        headers = self.token.headers()
        req_data = {
            "To": {
                "Address": email,
                "SubscriberKey": email,
                "ContactAttributes": {
                    "SubscriberAttributes": attrs
                },
            },
            "OPTIONS": {
                "RequestType": "SYNC"
            },
        }

        resp = requests.post(url, headers=headers, json=req_data)
        resp.raise_for_status()
        reply = resp.json()
        for response in reply['responses']:
            if response['hasErrors']:
                raven_client.captureMessage('Error occurred while submitting subscriber to exact target', extra=reply)
                error_messages = response.get('messageErrors', [])
                reg_messages = response.get('messages')
                # sometimes there are structured errors
                if len(error_messages):
                    raise exceptions.TriggeredSendException(error_messages[0]['messageErrorStatus'])
                # sometimes there are plain text errors
                elif len(reg_messages):
                    raise exceptions.TriggeredSendException(reg_messages[0])
                else:
                    raise exceptions.TriggeredSendException('Unknown TriggeredSend Error Occurred')
