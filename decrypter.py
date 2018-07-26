"""
Decrypter is responsible of decrypting the concatenated .ts file with openssl
"""
import sys
import logging
import subprocess as sp


class Decrypter:

    def __init__(self, dec_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and create a place holder for tool
        :param dec_logger: the logger assigned
        """
        self._tool = None
        self._logger = dec_logger

    def _convert_key(self) -> str:
        return bytearray.hex(bytearray(self._crypt_key_byte))

    def _check_tool(self) -> None:
        if sp.call(['which', self._tool], stdout=sp.DEVNULL):
            exit("abort: Cannot access decryption tool {}".format(self._tool))

    def decrypt(self) -> None:
        crypt_key_hex = self._convert_key()

        sp.call([self._tool, self._method, '-d', '-nosalt',
                 '-K', crypt_key_hex, '-iv', self._crypt_iv,
                 '-in', self._input, '-out', self._output])


# Sample
if __name__ == '__main__':
    minion = Decrypter(
        key=b'}}\x08\x90a\xaf\xe3\xfc\xfa\x9c\xd8\x15\xe6\xbb\xecC',
        iv='519dbb1e43a0ae6659b3993d6ea0e871',
        encrypted_file='encrypted.ts',
        decrypted_file='decrypted.ts')

    minion.decrypt()
