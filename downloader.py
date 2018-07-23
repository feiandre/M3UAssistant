"""
Downloader is responsible of downloading the links specified in the .m3u file to out_dir with aria2c
Multi-threads are used to save time, pool size is 8 by default
"""

import subprocess as sp

from typing import List

import threadpool

from .bcolours import BColours


class Downloader:

    def __init__(self, dow_logger: logging.Logger, pool_size: int = 8) -> None:
        """
        Welcoming the logger assigned, prepare thread pool,
        and create several place holder for class variables
        :param dow_logger: the logger assigned
        :param pool_size: the size of the thread pool
        """
        self._logger = dow_logger
        self._pool = threadpool.ThreadPool(pool_size)
        self._crr_num = self._ttl_num = 0
        self._tool = self._out_dir = None

    def check_tool(self, tool: str) -> None:
        """
        Checking if the download tool is available
        :param tool: the tool assigned for downloading
        """
        if sp.call(['which', tool], stdout=sp.DEVNULL):
            self._logger.error("abort: Cannot access download tool {}".format(tool))
            exit(2)
        self._tool = tool

    def download(self, links: List[str], out_dir: str = None) -> None:
        """
        Download the given links to output directory
        :param links: the links to the file to download
        :param out_dir: the output directory
        """
        self._out_dir, self._ttl_num = out_dir, len(links)

        download_requests = threadpool.makeRequests(self._download_thread, links)
        [self._pool.putRequest(req) for req in download_requests]
        self._pool.wait()
        print("Download complete")

    def _download_thread(self, link) -> None:
        """
        The download process for each thread, assuming using aria2c for now,
        keep reporting status
        :param link: the link to download from
        """
        self._report_status(current=self._crr_num, complete=self._ttl_num)
        command = '{} {}' \
                  ' --console-log-level=error' \
                  ' --download-result=hide' \
                  ' --show-console-readout false'.format(self._tool, link)
        if self._out_dir:
            command += ' --dir {}'.format(self._out_dir)

        sp.call(command.split())
        self._crr_num += 1

    @staticmethod
    def _report_status(current: int, complete: int) -> None:
        if not current:
            sys.stdout.write(BColours.HEADER
                             + 'Download started: Downloading {} items\n'.format(complete)
                             + BColours.END_COLOR)
            return

        if current == complete:
            sys.stdout.write(
                'Download completed: Downloaded {} items\n'.format(complete))
            return

        sys.stdout.write('Downloading ...'
                         + BColours.GREEN
                         + '{:.2f}%'.format(current / complete * 100)
                         + BColours.END_COLOR
                         + '({} items)\r'.format(current))

        sys.stdout.flush()


# Sample
if __name__ == '__main__':
    minion = Downloader(
        links=['https://get.videolan.org/vlc/2.2.6/macosx/vlc-2.2.6.dmg',
               'https://get.videolan.org/vlc/2.2.6/macosx/vlc-2.2.6.dmg',
               'https://get.videolan.org/vlc/2.2.6/macosx/vlc-2.2.6.dmg'])

    minion.download()
