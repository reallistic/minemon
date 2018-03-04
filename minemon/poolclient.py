""""
node-cryptonote-poool client
"""

import requests
import logging
import json
import re

logger = logging.getLogger(__name__)

RE_CONFIG_JS = re.compile(r'var ?([a-zA-Z0-9_]+) ?= ?(.+);')


class PoolClient:
    def __init__(self, pool_base='https://minexmr.com', config_path='config.js',
                 use_config=True, api_base=None, address=None):
        if not (use_config or api_base):
            logger.info(f'using "{pool_base}" for api')
            self._api_base = pool_base
        else:
            self._api_base = api_base

        self.pool_base = pool_base.rstrip('/')
        self.config_path = config_path.lstrip('/')
        self.use_config = use_config
        self.address = address

        self._config = {}
        self.session = requests.Session()

    @property
    def api_base(self):
        if not self._api_base:
            self._api_base = self.config.get('api')
            if self._api_base:
                self._api_base.rstrip('/')

        return self._api_base or self.pool_base

    @property
    def config(self):
        if not self._config and self.use_config:
            res = self.session.get(f'{self.pool_base}/{self.config_path}')
            res.raise_for_status()
            data = res.text
            config_matches = RE_CONFIG_JS.findall(data)
            for key, raw_value in config_matches:
                self._config[key] = json.loads(raw_value)

        return self._config

    def get_address_stats(self, address=None):
        address = address or self.address
        if not address:
            raise RuntimeError('No address provided')
        res = self.session.get(f'{self.api_base}/stats_address?address={address}')
        res.raise_for_status()
        return res.json()

    def get_stats(self):
        res = self.session.get(f'{self.api_base}/stats')
        res.raise_for_status()
        return res.json()

    def get_worker_stats(self, address=None):
        address = address or self.address
        if not address:
            raise RuntimeError('No address provided')
        res = self.session.get(f'{self.api_base}/get_wid_stats?address={address}')
        res.raise_for_status()
        return res.json()
