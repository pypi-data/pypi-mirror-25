from urllib.error import HTTPError
from sendgrid.sendgrid import SendGridAPIClient


class SendGridException(Exception):
    pass


class SendGrid(object):
    """
    A client wrapper for the Sendgrid python library.

    Takes in an `api_key` parameter, which is the API key you can get from the Sendgrid dashboard.
    The `send()` method accepts the JSON-formatted message that needs to be sent.
    """
    def __init__(self, api_key):
        self.client = SendGridAPIClient(apikey=api_key).client

    def send(self, message):
        try:
            self.client.mail.send.post(request_body=message)
        except HTTPError as exc:
            raise SendGridException('SendGrid API responded with HTTP %r: %r' % (exc.code, exc.reason))
