"""
Downloader is responsible of downloading the links specified in the .m3u file to out_dir with aria2c
Multi-threads are used to save time, pool size is 8 by default
"""

import subprocess as sp

from typing import List

from .bcolours import BColours


class Downloader:

    def __init__(self, links: List[str], out_dir: str=None, tool: str='aria2c'):
        self._links = links
        self._tool = tool
        self._dir = out_dir

    def _check_tool(self) -> None:
        if sp.call(['which', self._tool], stdout=sp.DEVNULL):
            exit("abort: Cannot access download tool {}".format(self._tool))

    def download(self):
        current = -1
        self._report_status(current=current, complete=len(self._links))

        for link in self._links:
            current += 1
            self._report_status(current=current, complete=len(self._links))

            command = [self._tool,
                       link,
                       '--console-log-level=error',
                       '--download-result=hide',
                       '--show-console-readout', 'false']
            command = command + ['--dir', self._dir] if self._dir else command

            sp.call(command)

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
