# coding: utf-8

import os

from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.easymp4 import EasyMP4


def tag_in_file(file, tag):
    extension = os.path.splitext(file)[1][1:]

    if extension == 'flac':
        tags = FLAC(file)
    elif extension == 'ogg':
        tags = OggVorbis(file)
    elif extension == 'mp3':
        tags = EasyID3(file)
    elif extension == 'mpc':
        tags = APEv2(file)
    elif extension in ['mp4', 'm4a']:
        tags = EasyMP4(file)
    else:
        return None, None

    return tag in tags
