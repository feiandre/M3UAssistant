# M3UAssistant

Nowadays, video websites tend to break their online videos into hundreds (if not thousands) of TS fragments and stream them via an M3U playlist.
This makes scraping rather hard as:

1. Without access to the M3U playlist, we don't know how many files are there and what their names are
2. Each TS fragment can be encrypted
3. TS is not that popular hence might not be correctly recognised by many video players
4. Hundreds of TS files are not watchable for humans at all

M3UAssistant is designed to address this problem by:

1. Parsing the content (i.e. TS fragment URLs) of the target M3U8 file, and the key file if the TS fragments are encrypted
2. Download the fragments and the value of decryption key if encrypted
3. Concatenate fragments into one TS file
4. Decrypt the TS file
5. Convert the decrypted file to MP4, which can be recognised by all most all video player


## Dependencies
Unfortunately, all of the following dependencies are required for now.
In the short (hopefully) future, I will add the options of replacing them with other ones you would like to use.

However, hey, it is always nice to have a try on the following ones on this or other occasions if you haven't : )

### Built-in dependencies

Hopefully, your computer already has the tool for concatenation: [`cat`](http://www.linfo.org/cat.html)

### pip3 dependencies

```bash
pip3 install -r requirements.txt
```

### Other dependencies

The following dependencies can be installed via [`HomeBrew`](https://brew.sh/):

* For downloading: [`aria2c`](https://aria2.github.io/):
```bash
brew install aria2c
```

* For decryption: [`OpenSSL`](https://www.openssl.org/):

```bash
brew install openssl
```

* For video conversion: [`FFmpeg`](https://www.ffmpeg.org/)
```bash
brew install ffmpeg
```

If you are not a `macOS` user, then good luck on finding them via your own package manager :P
