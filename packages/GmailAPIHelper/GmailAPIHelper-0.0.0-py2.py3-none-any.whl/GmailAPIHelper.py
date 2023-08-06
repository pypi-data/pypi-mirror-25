"""
Module to help navigate the Gmail API responses
"""

__version__ = '0.0.0'

import os
import re
from datetime import datetime
from base64 import urlsafe_b64decode
import httplib2
from pytz import utc
from apiclient import discovery
from oauth2client import client, tools, file


class GmailHelper:
    """
    Helper class
    """
    def __init__(self, app_name):
        """
        Creates/loads credentials for the Gmail API connection

        Args:
            : app_name: Application name as defined during pre-setup:
                        https://developers.google.com/gmail/api/quickstart/python
        """
        self.app_name = app_name
        self.creds = self.setup()
        self.service = discovery.build('gmail', 'v1',
                                       http=self.creds.authorize(httplib2.Http()))

    def setup(self):
        """
        Sets up credentials to access the Gmail API if they don't exist

        Returns:
               : credentials
        """
        home_dir = os.path.expanduser('~')
        secret_file = os.path.join(home_dir, "client_secret.json")
        scopes_url = "https://mail.google.com/"
        credential_path = os.path.join(home_dir, "gmail-credentials.json")
        store = file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(secret_file,
                                                  scopes_url)
            flow.user_agent = self.app_name
            credentials = tools.run_flow(flow, store)
        return credentials

    def _message_contents(self, msg_id):
        """
        Retrieves the contents of a message, by ID

        Args:
            : msg_id: Gmail message ID

        Returns:
               : Contents of the message
        """
        messages = self.service.users().messages()
        message_contents = messages.get(userId="me", id=msg_id).execute()
        return message_contents

    def _walk(self, payload):
        """
        Warning: This is a recursive function. It calls on itself until
                 it can get a result, may hang if can't complete

        Walks the contents of a Gmail message payload to find the 'text/plain'
        or 'text/html' MimeType message

        Args:
            : payload: GmailMessage['payload']

        Returns:
               : Base64-encoded plain text or html message
        """
        for part in payload['parts']:
            if 'text/' in part['mimeType']:
                data = part['body']['data']
                return data
            return self._walk(part)

    def _retrieve(self, message):
        """
        Retrieves the pieces of content from a Gmail message

        Exceptions:
                  : AttributeError if a piece of content couldn't be retrieved

        Returns:
               : Dictionary with ID, Datetime, From and Message
        """
        content = {}
        content['id'] = message['id']
        _date = int(message['internalDate'])
        _date = utc.localize(datetime.fromtimestamp(_date/1000))
        content['date'] = utc.normalize(_date)
        payload = message['payload']
        for header in payload['headers']:
            if header['name'].lower() == 'from':
                _from = header['value']
        email_encoded = re.search('<(.*?)>', _from)
        if email_encoded:
            _from = email_encoded.group(1)
        content['from'] = _from
        if 'parts' in payload:
            data = self._walk(payload)
        else:
            data = payload['body']['data']
        data = urlsafe_b64decode(data.encode("ASCII"))
        content['message'] = data.decode('utf-8')
        expected_content = set(['id', 'date', 'from', 'message'])
        found_content = set([c for c in content])
        missing_content = expected_content.difference(found_content)
        if missing_content:
            raise AttributeError(f'{missing_content} was not retrieved')
        return content

    def get_emails(self, search, max_results=None):
        """
        Retrieve latest e-mails (up to 100) found by a search

        Args:
            : search: Search to send to Gmail. Accepts same special strings
                      such as 'from:*****' or 'in:sent'
            : max_results: Max number of results (up to 100).
                           Recommended

        Returns:
               : List of e-mail dictionaries with:
                       'id'      : message id
                       'date'    : UTC datetime of the e-mail
                       'from'    : Sender e-mail
                       'message' : Plain text or HTML message
        """
        search = self.service.users().messages().list(userId="me",
                                                      q=search,
                                                      maxResults=max_results)
        results = search.execute()
        msg_ids = [msg['id'] for msg in results['messages']]
        messages = list(map(self._message_contents, msg_ids))
        emails = list(map(self._retrieve, messages))
        return emails
