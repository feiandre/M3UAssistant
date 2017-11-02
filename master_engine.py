import re
import subprocess as sp
from fetcher import Fetcher
from parser import Parser
from downloader import Downloader
from decrypter import Decrypter
from allocator import Allocator
from typing import List, Dict, Any


class MasterEngine:

    _Master_Name = 'M3U Assistant'

    def __init__(self, args=None):

        self._par_minion = Parser(my_master=self._Master_Name)
        self._fet_minion = Fetcher()
        self._dow_minion = None
        self._dec_minion = None
        self._alc_minion = None

        self._m3u_dict = {}
        # parse args
        if args:
            self._args_parsed = args
        else:
            all_args = self._par_minion.prepare_args()
            self._args_parsed = all_args.parse_args()
        self._out_file = self._args_parsed.output_name
        self._out_dir = re.match("(.*)/(.*).mp4",
                                 self._out_file).group(1)

    def preparing(self) -> Dict[str, Any]:
        # Fetch m3u
        content_bytes = self._fet_minion.fetch_m3u(
            m3u_url=self._args_parsed.m3u_url[0])

        # Parse m3u
        self._m3u_dict = self._par_minion.parse_m3u(
            m3u_content_bytes=content_bytes)

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
    master.preparing()
    master.downloading(urls=['http://sample01.ts', 'http://sample02.ts'])
    # master.finishing(key_url=key_url,
    #                  input_files=['./ts/01.ts', './ts/02.ts'],
    #                  out_name='./out.mp4')
