"""
A Fetcher that is responsible of fetching (i.e. requesting) contents (e.g. M3U8, Key)
from given URL
"""

import sys
import logging
import requests


class Fetcher:

    def __init__(self, fet_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned
        :param fet_logger: the logger assigned
        """
        self._logger = fet_logger

    def fetch_m3u(self, m3u_url: str) -> bytes:
        """
        Fetching the content of M3U8 and return it
        :param m3u_url: the URL to M3U8 file
        :return: the content of M3U8 in bytes
        """
        m3u_content = requests.get(url=m3u_url).content
        self._logger.debug('M3U8 content: {}'.format(m3u_content))
        return m3u_content

    def fetch_key(self, key_url: str=None) -> bytes:
        """
        Fetching the content of key and return it
        :param key_url: the URL to key file
        :return: the content of key in bytes
        """
        self._logger.debug('Key URL: {}'.format(key_url))
        key_content = requests.get(url=key_url).content if key_url else None
        self._logger.debug('Key content: {}'.format(key_content))
        return key_content


# Demo
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    minion = Fetcher(logger)
    print(minion.fetch_m3u("http://sample.m3u8"))
    print(minion.fetch_key("http://sample.key"))
