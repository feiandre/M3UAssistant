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
