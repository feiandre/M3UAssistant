# Optional: concatenate all .ts files to one and convert it to .mp4
import os
import subprocess as sp
from typing import List


class Allocator:

    def __init__(self, input_files: List[str],
                 conversion_tool: str='ffmpeg', concatenation_tool: str='cat'):
        self._input = input_files
        self._conversion_tool = conversion_tool
        self._concatenation_tool = concatenation_tool
        self._check_tool()

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
