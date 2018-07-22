"""
The Master Engine of M3UAssistant, arrange minions to
download M3U file, read content, download all files inside, decrypt them if necessary and
concatenate them
"""

import logging
import re
import subprocess as sp
import sys
from argparse import Namespace
from logging import Logger
from typing import List, Dict

from .allocator import Allocator
from .decrypter import Decrypter
from .downloader import Downloader
from .fetcher import Fetcher
from .parser import Parser


class MasterEngine:

    def __init__(self) -> None:
        """
        Prepare the minions, the dictionary for the content of M3U8 and an indicator of encryption
        """
        self._prepare_minions()
        self._m3u_dict = {}
        self._encrypted = False

    @staticmethod
    def _prepare_logger() -> Logger:
        """
        Create a logger minion that will print messages via stdout
        :return: logger
        """
        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        return logger

    def _prepare_minions(self) -> None:
        """
        Call out the minions and send logger minion to monitor
        """
        self._log_minion = self._prepare_logger()
        self._par_minion = Parser(par_logger=self._log_minion)
        self._fet_minion = Fetcher(fet_logger=self._log_minion)
        self._dow_minion = Downloader(dow_logger=self._log_minion)
        self._dec_minion = Decrypter(dec_logger=self._log_minion)
        self._alc_minion = Allocator(alc_logger=self._log_minion)

    def assist(self) -> None:
        """
        Parses M3U, downloads all files and convert to one playable MP4 file
        """
        args = self._par_minion.prepare_args()
        m3u_url = args.m3u_url[0]
        m3u_prefix = args.m3u_prefix[0]
        out_file = args.output_name
        out_dir = re.match("(.*)/(.*).mp4", out_file).group(1)

        self._m3u_dict = self._parse_m3u(m3u_url=m3u_url)
        key_bytes = self._parse_key(prefix=m3u_prefix,
                                    key_uri=self._m3u_dict.get('enc').get('uri').strip('"'))
        self._check_tools(args=args)
        self._download(prefix=m3u_prefix, out_dir=out_dir)
        self._finish_up(out_dir=out_dir, final_name=out_file, key_bytes=key_bytes)

        return self._m3u_dict

    def feed_key(self, key_url: str):
        self._args_parsed.key_url = key_url

    def feed_out_name(self, out_name: str):
        self._args_parsed.output_name = out_name

    def downloading(self, urls: List[str]):
        if self._m3u_dict['key'] and not self._args_parsed.key_url:
            exit("Abort: The .ts files are encrypted, "
                 "please ensure you have feed the key before downloading")

        self._dow_minion = Downloader(links=urls, out_dir=self._out_dir)
        self._dow_minion.download()

    def finishing(self, encryption_method: str=None):

        file_names = sp.Popen(['ls', self._out_dir], stdout=sp.PIPE)

        input_files = ["{}/{}".format(self._out_dir, str(name, 'utf-8'))[:-1]
                       for name in file_names.stdout.readlines()]

        # print("Files = {}".format(input_files))

        # Concatenate
        self._alc_minion = Allocator(input_files=input_files)
        concatenated_name = self._alc_minion.concatenate(
            out_name=self._out_file)

        # Decrypt
        key_bytes = self._fet_minion.fetch_key(self._args_parsed.key_url)

        iv = self._m3u_dict['key']['iv']
        decrypted_file_name = self._out_file[:-3]+'ts'
        self._dec_minion = Decrypter(key=key_bytes, iv=iv,
                                     encrypted_file=concatenated_name,
                                     decrypted_file=decrypted_file_name,
                                     encryption_method=encryption_method)
        self._dec_minion.decrypt()

        # Convert
        self._alc_minion.convert(in_ts=decrypted_file_name,
                                 out_mp4=self._out_file)


# Sample
if __name__ == '__main__':
    master = MasterEngine()
    master.assist()
