# coding: utf-8
from __future__ import absolute_import, unicode_literals

import traceback
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from timezone_logging.timezone_logging import get_timezone_logger

class KnowruClient(object):
    def __init__(self, token, knowru_url='https://www.knowru.com', retry_total=3, backoff_factor=1, status_forcelist=(502, 503, 504), method_whitelist=('GET', 'POST')):
        if knowru_url.endswith('/'):
            knowru_url = knowru_url[:-1]
        self.knowru_url = knowru_url
        self._token = token
        self.headers = {'Authorization': 'Token {}'.format(token), 'Content-Type': 'application/json', 'Accept': 'application/json'}
        self._retry_total = retry_total
        self._backoff_factor = backoff_factor
        self._status_forcelist = status_forcelist
        self._method_whitelist = method_whitelist
        self._adapter = HTTPAdapter(max_retries=Retry(total=retry_total, backoff_factor=backoff_factor, status_forcelist=status_forcelist, method_whitelist=method_whitelist))
        self.session = requests.Session()
        self.session.mount(knowru_url, self._adapter)

    def run_runnable(self, runnable_name, input_data, output_if_error=None):
        try:
            r = self.session.post('{}/api/runnable/{}/run.json/'.format(self.knowru_url, runnable_name), json={'input': input_data}, headers=self.headers)
        except Exception as e:
            logger = get_timezone_logger('KnowruClient.call_runnable')
            logger.error(traceback.format_exc())
            if output_if_error is not None:
                return output_if_error
            else:
                raise e
        else:
            return r.json()['output']