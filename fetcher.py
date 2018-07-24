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

    @staticmethod
    def fetch_m3u(m3u_url: str, params: Dict[str, str]=None) -> bytes:
        m3u_response = requests.get(url=m3u_url, params=params)
        return m3u_response.content

    @staticmethod
    def fetch_key(key_url: str=None) -> bytes:
        key_response = requests.get(url=key_url) if key_url else None
        return key_response.content if key_response else None


# Demo
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    minion = Fetcher(logger)
    print(minion.fetch_m3u("http://sample.m3u8"))
    print(minion.fetch_key("http://sample.key"))
