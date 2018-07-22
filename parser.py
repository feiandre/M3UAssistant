"""
A parser that is responsible of:
1. parse command line arguments,
2. parse links/key info from the bytes of responded .m3u,
3. parse key bytes from the the bytes of responded .key
"""

import logging
import re
import requests

from argparse import ArgumentParser
from typing import Dict, Any


class Parser:
    _KEY_HEADER = '#EXT-X-KEY:'

    def __init__(self, par_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and prepare the command line argument parser
        :param par_logger: the logger assigned
        """
        self._logger = par_logger
        self.arg_parser = ArgumentParser(description="parses the cml arguments")

    def parse_args(self) -> Namespace:
        """
        parsing arguments and return them
        :return: the arguments in a Namespace
        """
        self.arg_parser.add_argument(
            'm3u_url', nargs=1, type=str,
            help="the url to the .m3u file, e.g. http://sample.m3u")

        self.arg_parser.add_argument(
            '--key_url', '-K', metavar='key_url', nargs='?', type=str,
            help="the url to the .key file, e.g. http://sample.key")

        self.arg_parser.add_argument(
            '--output_name', '-O', metavar='out', nargs='?', type=str,
            default='./mp4/out.mp4',
            help="the dir and the name of the output file, e.g. ./mp4/out.mp4")

        self.arg_parser.add_argument(
            '--verbose', '-V', metavar='debug', nargs='?', type=str,
            help="Whether to print out the notifications")

        return args

    def parse_m3u(self, m3u_content_bytes: bytes) -> Dict[str, Any]:

        self._m3u_content = str(m3u_content_bytes, 'utf-8').split('\n')

        for line in self._m3u_content:
            if not line:
                continue

            if not self._key_dict and (self._KEY_HEADER in line):
                # Encrypted, start from this line with key info
                self._parse_key_uri(key_line=line)

            self._parse_links(link_line=line)

        return {'links': self._links, 'key': self._key_dict}

    def _parse_links(self, link_line: str) -> None:
        if link_line[0] == '#':
            return
        # Partial urls
        self._links.append(link_line)

    def _parse_key_uri(self, key_line: str):
        key_pattern = r'#EXT-X-KEY:METHOD=(?P<method>.*),' \
                      r'URI=(?P<uri>.*),' \
                      r'IV=(?P<iv>.+)' \
            if 'IV' in key_line else \
            r'#EXT-X-KEY:METHOD=(?P<method>.*),' \
            r'URI=(?P<uri>.*),'

        self._key_dict = re.match(key_pattern, key_line).groupdict()

    @staticmethod
    def parse_key_file(key_content_bytes: bytes):
        return str(key_content_bytes, 'utf-8')


# Sample
if __name__ == '__main__':
    request_url = "http://sample.m3u8"
    response = requests.get(url=request_url)

    minion = Parser(my_master="Master")
    print(minion.parse_m3u(m3u_content_bytes=response.content))
