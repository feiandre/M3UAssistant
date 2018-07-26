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

    def _convert_key(self, key_bytes: bytes) -> str:
        """
        Converting key from bytes to hex value
        :param key_bytes: the key bytes to convert
        :return: the converted hex in str
        """
        key_hex = bytearray.hex(bytearray(key_bytes))
        self._logger.debug('key_hex = {}'.format(key_hex))
        return key_hex

    def _check_tool(self) -> None:
        if sp.call(['which', self._tool], stdout=sp.DEVNULL):
            exit("abort: Cannot access decryption tool {}".format(self._tool))

    def decrypt(self) -> None:
        crypt_key_hex = self._convert_key()

        sp.call([self._tool, self._method, '-d', '-nosalt',
                 '-K', crypt_key_hex, '-iv', self._crypt_iv,
                 '-in', self._input, '-out', self._output])


# Demo
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    minion = Decrypter(logger)

    minion.decrypt(
        iv='519dbb1e43a0ae6659b3993d6ea0e871',
        key_bytes=b'}}\x08\x90a\xaf\xe3\xfc\xfa\x9c\xd8\x15\xe6\xbb\xecC',
        out_name='decrypted.ts',
        encrypted_file='encrypted.ts', encryption_method='AES-128')
