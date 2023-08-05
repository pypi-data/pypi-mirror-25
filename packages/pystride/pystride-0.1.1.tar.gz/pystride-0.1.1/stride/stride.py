import json
from time import time

import requests

BEARER_TOKEN_URL = 'https://auth.atlassian.com/oauth/token'
SITE_API_URL = 'https://api.atlassian.com/site'

class Stride:
    def __init__(self, cloud_id, client_id, client_secret):
        self.cloud_id = cloud_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = None
        self._access_token_expires = 0

    @property
    def access_token(self):
        if self._access_token and self._access_token_expires > time():
            return self._access_token
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'audience': 'api.atlassian.com'
        }
        r = requests.post(BEARER_TOKEN_URL, json=payload)
        r.raise_for_status()
        data = json.loads(r.text)
        self._access_token = data['access_token']
        self._access_token_expires = time() - 60 + int(data['expires_in'])
        return self._access_token

    @property
    def headers(self):
        headers = {
            'authorization': f'Bearer {self.access_token}'
        }
        return headers

    def get_room_id(self, room_name):
        params = {'query': room_name}
        r = requests.get(f'{SITE_API_URL}/{self.cloud_id}/conversation',
                         params=params, headers=self.headers)
        r.raise_for_status()
        data = json.loads(r.text)
        for room in data['values']:
            if room['name'] == room_name:
                return room['id']
        return None

    def message_room(self, room_id, message_doc):
        r = requests.post(f'{SITE_API_URL}/{self.cloud_id}/conversation/{room_id}/message',
                          json=message_doc, headers=self.headers)
        r.raise_for_status()
        return r

    def message_user(self, user_id, message_doc):
        r = requests.post(f'{SITE_API_URL}/{self.cloud_id}/conversation/user/{user_id}/message',
                          json=message_doc, headers=self.headers)
        r.raise_for_status()
        return r
