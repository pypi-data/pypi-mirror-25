
import os
import sys
import json
import requests
import logging

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from requests.auth import AuthBase

LOG = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 86400


class ApiAuth(AuthBase):

    def __init__(self, key):

        self.key = key

    def __call__(self, r):

        r.headers['Authorization'] = 'Key %s' % self.key
        return r


class ApiClient(object):

    def __init__(self, endpoint=None, key=None, timeout=5.0, ssl_verify=True):

        self.endpoint = endpoint or os.environ.get('ALERTA_ENDPOINT', "http://localhost:8080")
        self.key = key or os.environ.get('ALERTA_API_KEY', '')

        self.session = requests.Session()
        self.session.verify = ssl_verify  # or use REQUESTS_CA_BUNDLE env var

        self.timeout = float(timeout)

    def __repr__(self):

        return 'ApiClient(endpoint=%r, key=%r)' % (self.endpoint, self.key)

    def get_alerts(self, query=None):

        return self._get('/alerts', query)

    def get_counts(self, query=None):

        return self._get('/alerts/count', query)

    def get_history(self, query=None):

        return self._get('/alerts/history', query)

    def send_alert(self, alert):

        return self._post('/alert', data=str(alert))

    def send(self, msg):

        if msg.event_type == 'Heartbeat':
            return self.send_heartbeat(msg)
        else:
            return self.send_alert(msg)

    def get_alert(self, alertid):

        return self._get('/alert/%s' % alertid)

    def tag_alert(self, alertid, tags):

        if not isinstance(tags, list):
            raise

        return self._put('/alert/%s/tag' % alertid, data=json.dumps({"tags": tags}))

    def untag_alert(self, alertid, tags):

        if not isinstance(tags, list):
            raise

        return self._put('/alert/%s/untag' % alertid, data=json.dumps({"tags": tags}))

    def open_alert(self, alertid, text=''):

        self.update_status(alertid, 'open', text)

    def ack_alert(self, alertid, text=''):

        self.update_status(alertid, 'ack', text)

    def unack_alert(self, alertid, text=''):

        self.open_alert(alertid, text)

    def assign_alert(self, alertid, text=''):

        self.update_status(alertid, 'assigned', text)

    def close_alert(self, alertid, text=''):

        self.update_status(alertid, 'closed', text)

    def update_status(self, alertid, status, text):

        return self._put('/alert/%s/status' % alertid, data=json.dumps({"status": status, "text": text}))

    def delete_alert(self, alertid):

        return self._delete('/alert/%s' % alertid)

    def send_heartbeat(self, heartbeat):
        """
        Send a heartbeat
        """
        return self._post('/heartbeat', data=str(heartbeat))

    def get_heartbeats(self):
        """
        Get list of heartbeats
        """
        return self._get('/heartbeats')

    def delete_heartbeat(self, heartbeatid):

        return self._delete('/heartbeat/%s' % heartbeatid)

    def get_top10(self, group='event'):

        return self._get('/alerts/top10', {'group-by': group})

    def blackout_alerts(self, blackout):
        """
        Define a blackout period
        """
        return self._post('/blackout', data=json.dumps(blackout))

    def get_blackouts(self):
        """
        Get list of blackouts
        """
        return self._get('/blackouts')

    def delete_blackout(self, blackoutid):

        return self._delete('/blackout/%s' % blackoutid)

    def get_users(self, query=None):

        return self._get('/users', query)

    def update_user(self, user, data):

        return self._put('/user/%s' % user, data=json.dumps(data))

    def create_key(self, key):

        return self._post('/key', data=json.dumps(key))

    def get_keys(self):

        return self._get('/keys')

    def revoke_key(self, key):

        return self._delete('/key/%s' % key)

    def get_status(self):

        return self._get('/management/status')

    def _get(self, path, query=None):

        query = query or tuple()

        url = self.endpoint + path + '?' + urlencode(query, doseq=True)

        try:
            response = self.session.get(url, auth=ApiAuth(self.key), timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            sys.exit(1)

        LOG.debug('Request Headers: %s', response.request.headers)

        LOG.debug('Response Headers: %s', response.headers)
        LOG.debug('Response Body: %s', response.text)

        return self._handle_error(response)

    def _post(self, path, data=None):

        url = self.endpoint + path
        headers = {'Content-Type': 'application/json'}

        try:
            response = self.session.post(url, data=data, headers=headers, auth=ApiAuth(self.key), timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            sys.exit(1)

        LOG.debug('Request Headers: %s', response.request.headers)
        LOG.debug('Request Body: %s', data)

        LOG.debug('Response Headers: %s', response.headers)
        LOG.debug('Response Body: %s', response.text)

        return self._handle_error(response)

    def _put(self, path, data=None):

        url = self.endpoint + path
        headers = {'Content-Type': 'application/json'}

        try:
            response = self.session.put(url, data=data, headers=headers, auth=ApiAuth(self.key), timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            sys.exit(1)
        LOG.debug('Request Headers: %s', response.request.headers)
        LOG.debug('Request Body: %s', data)

        LOG.debug('Response Headers: %s', response.headers)
        LOG.debug('Response Body: %s', response.text)

        return self._handle_error(response)

    def _delete(self, path):

        url = self.endpoint + path

        try:
            response = self.session.delete(url, auth=ApiAuth(self.key), timeout=self.timeout)
        except requests.exceptions.RequestException as e:
            LOG.error(e)
            sys.exit(1)

        LOG.debug('Request Headers: %s', response.request.headers)

        LOG.debug('Response Headers: %s', response.headers)
        LOG.debug('Response Body: %s', response.text)

        return self._handle_error(response)

    @staticmethod
    def _handle_error(response):
        resp = response.json()
        status = resp.get('status', None)
        if status == 'ok':
            return resp
        if status == 'error':
            print()
            LOG.error(resp.get('message', 'Unhandled API error response'))
            sys.exit(1)
        return resp
