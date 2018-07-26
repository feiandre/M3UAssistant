"""
Decrypter is responsible of decrypting the concatenated .ts file with openssl
"""
import logging
import subprocess as sp
import sys


class Decrypter:

    def __init__(self, dec_logger: logging.Logger) -> None:
        """
        Welcoming the logger assigned and create a place holder for tool
        :param dec_logger: the logger assigned
        """
        self._tool = None
        self._logger = dec_logger

    def check_tool(self, tool: str) -> None:
        """
        Checking if the tool is available
        :param tool: the tool assigned for decryption
        """
        if sp.call(['which', tool], stdout=sp.DEVNULL):
            self._logger.error("abort: Cannot access decryption tool {}".format(tool))
            exit(2)
        self._tool = tool

    def decrypt(self, iv: str, key_bytes: bytes, encrypted_file: str, encryption_method: str,
                out_name: str = None) -> None:
        """
        Decrypting the encrypted_file with the tool assigned and the info in params
        :param iv: initial vector
        :param key_bytes: decryption key
        :param encrypted_file: the file to decrypt
        :param encryption_method: the method in which the file is encrypted
        :param out_name: the desired output name of the decrypted file
        """
        if not (key_bytes and self._tool):
            self._logger.error(
                "abort: Files in M3U8 are encrypted but missing key_bytes {}".format(key_bytes))
            exit(1)
        key_hex = self._convert_key(key_bytes=key_bytes)
        dec_command = '{tool} {enc_method} -d -nosalt ' \
                      '-K {key_hex} -iv {iv} -in {enc_file} -out {dec_file}' \
            .format(tool=self._tool, enc_method=encryption_method,
                    key_hex=key_hex, iv=iv, enc_file=encrypted_file,
                    dec_file=out_name)

        sp.call(dec_command.split(' '))
        self._logger.debug('decryption command: {}'.format(dec_command))

    def _convert_key(self, key_bytes: bytes) -> str:
        """
        Converting key from bytes to hex value
        :param key_bytes: the key bytes to convert
        :return: the converted hex in str
        """
        key_hex = bytearray.hex(bytearray(key_bytes))
        self._logger.debug('key_hex = {}'.format(key_hex))
        return key_hex


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
