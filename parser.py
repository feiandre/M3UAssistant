"""
A parser that is responsible of:
1. parse command line arguments,
2. parse links/key info from the bytes of responded .m3u,
3. parse key bytes from the the bytes of responded .key
"""

import logging
import re
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Dict, Any


class Parser:
    _KEY_HEADER = '#EXT-X-KEY:'
    _ENC_PATTERN_1 = r'#EXT-X-KEY:METHOD=(?P<method>.*),URI=(?P<uri>.*)'
    _ENC_PATTERN_2 = r'#EXT-X-KEY:METHOD=(?P<method>.*),URI=(?P<uri>.*),IV=(?P<iv>.+)'

    def __init__(self, par_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and prepare the command line argument parser
        :param par_logger: the logger assigned
        """
        self._logger = par_logger
        self.arg_parser = ArgumentParser(description="parses the cml arguments")

    def parse_args(self) -> Namespace:
        """
        Parsing arguments and return them
        :return: the arguments in a Namespace
        """
        self.arg_parser.add_argument(
            'm3u_url', nargs=1, type=str,
            help="the url to the .m3u file, e.g. http://sample.m3u")

        self.arg_parser.add_argument(
            '--m3u_prefix', '-P', nargs=1, type=str,
            help="the prefix of each url in the .m3u file")

        self.arg_parser.add_argument(
            '--output_name', '-O', nargs='?', type=str,
            default='./out/out.mp4',
            help="the path to the output MP4 file, e.g. ./out/out.mp4")

        self.arg_parser.add_argument(
            '--verbose', '-V', nargs='?', type=bool,
            default=False,
            help="Whether to print out the logging messages")

        self.arg_parser.add_argument(
            '--dow_tool', '-W', nargs='?', type=str,
            help="Coming soon: "
                 "the tool for downloading, e.g. aria2c, which will be used as default")

        self.arg_parser.add_argument(
            '--dec_tool', '-D', nargs='?', type=str,
            help="Coming soon: "
                 "the tool for decryption, e.g. openssl, which will be used as default")

        self.arg_parser.add_argument(
            '--cov_tool', '-C', nargs='?', type=str,
            help="Coming soon: "
                 "the tool to convert .ts files to the ideal format, "
                 "e.g. FFmpeg, which will be used as default")

        self.arg_parser.add_argument(
            '--cat_tool', '-T', nargs='?', type=str,
            help="Coming soon: "
                 "the tool to concat all fragment files in M3U8 to one, "
                 "e.g. cat, which will be used as default")

        args = self.arg_parser.parse_args()
        self._logger.setLevel(level=logging.DEBUG if args.verbose else logging.WARN)
        self._logger.debug('Arguments parsed: {}'.format(args))

        return args

    def parse_m3u(self, contents_bytes: bytes) -> Dict[str, Any]:
        """
        Parsing the byte content of the M3U8 file to a dictionary
        :param contents_bytes: the content of M3U8 in bytes
        :return: the dictionary containing info of M3U8
        """
        enc_dict, links = {}, []
        content_list = str(contents_bytes, 'utf-8').split('\n')

        for content in content_list:
            if not content:
                continue
            if self._KEY_HEADER in content:
                enc_dict = self._parse_key_line(key_line=content)

            self._parse_links(link_line=content, links=links)

        self._logger.debug("M3U8 Links = {links}\nM3U8 Enc_dict={enc_dict}"
                           .format(links=links, enc_dict=enc_dict))

        return {'links': links, 'enc': enc_dict}

    def _parse_key_line(self, key_line: str) -> Dict[str, str]:
        """
        Parsing the line containing key information and return the information in a dictionary
        :param key_line: the line containing key info
        :return: the dictionary of key and other info might be useful for decryption
        """
        enc_pattern = self._ENC_PATTERN_2 if 'IV' in key_line else self._ENC_PATTERN_1

        enc_dict = re.match(enc_pattern, key_line).groupdict()
        self._logger.debug('enc_dict parsed: {}'.format(enc_dict))
        return enc_dict

    def _parse_links(self, link_line: str, links: List[str]) -> None:
        """
        Parsing the lines containing the links to all files in M3U8 and store it to a list
        :param link_line: the line containing links to download
        :param links: all links parsed
        """
        if link_line[0] == '#':
            return
        self._logger.debug('Link parsed: {}'.format(link_line))
        links.append(link_line)


# Demo
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    minion = Parser(par_logger=logger)
    print(minion.parse_m3u(contents_bytes=b'Test\n'))
