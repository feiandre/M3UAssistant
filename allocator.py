"""
Allocator is responsible of:
1. concatenating .ts file fragments into one, and
2. converting .ts file to .mp4
"""


import os
import sys
import logging
import subprocess as sp
from typing import List


class Allocator:

    def __init__(self, alc_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and create place holders for tools
        :param alc_logger: the logger assigned
        """
        self._logger = alc_logger
        self.cov_tool = None
        self.cat_tool = None

    def _check_tool(self) -> None:
        if sp.call(['which', self._conversion_tool], stdout=sp.DEVNULL):
            exit("abort: Cannot access conversion tool {}"
                 .format(self._conversion_tool))

        if (len(self._input) > 1)\
                and sp.call(['which',
                             self._concatenation_tool], stdout=sp.DEVNULL):
            exit("abort: Cannot access concatenation_tool tool {}"
                 .format(self._concatenation_tool))

    def concatenate(self, out_name: str) -> str:
        if len(self._input) == 1:
            return self._input[0]

        concatenated_name = '{}_en.ts'.format(out_name[:-4])

        command = [self._concatenation_tool] \
            + self._input \
            + ['>', concatenated_name]

        os.system(" ".join(command))
        return concatenated_name

    def convert(self, in_ts: str, out_mp4: str) -> None:

        command = [self._conversion_tool,
                   '-i', in_ts,
                   '-codec', "copy",
                   out_mp4]
        sp.call(command)


# Sample
if __name__ == '__main__':
    minion = Allocator(input_files=['01.ts', '02.ts', '03.ts'])
    name = minion.concatenate(out_name="out.ts")
    minion.convert(in_ts=name, out_mp4="out.mp4")
