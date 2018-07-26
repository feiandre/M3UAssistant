"""
Decrypter is responsible of decrypting the concatenated .ts file with openssl
"""

import subprocess as sp


class Decrypter:

    def __init__(self, key: bytes, iv: str,
                 encrypted_file: str, decrypted_file: str=None,
                 encryption_method: str=None, tool: str='openssl'):
        self._crypt_key_byte = key
        self._crypt_iv = iv[2:] if "0x" == iv[:2] else iv
        self._input = encrypted_file
        self._output = decrypted_file if decrypted_file else 'dec.ts'
        self._method = encryption_method if encryption_method else 'aes-128-cbc'
        self._tool = tool
        self._check_tool()

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
