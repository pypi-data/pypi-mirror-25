#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import base64
import datetime as dt
import logging
import os
import sys
import urllib
import urllib2

from sibus_lib.utils import exec_process

__author__ = 'Alex'

logger = logging.getLogger()

class TextToSpeech:
    TTS_URL = 'http://api.voicerss.org/?'
    DOC_URL = "http://www.voicerss.org/api/documentation.aspx"
    APIKEY = "52a168f7eeb74d2ba633eb074453f66c"

    def __init__(self, text, lang='fr-fr', tmp_dir="/tmp/voiceRSS/tts", debug=False):
        self.FILEDIR = tmp_dir
        if not os.path.isdir(self.FILEDIR):
            os.makedirs(self.FILEDIR)

        self.debug = debug
        self.lang = lang
        self.set_text(text)

    def set_text(self, text):
        if not text:
            raise Exception('No text to speak')

        text = text.replace('\n', '').strip()

        logger.info("Set TTS text: '%s'" % text)

        if not len(text):
            raise Exception('Empty text !')

        self._audio_data = None
        self._text = text
        self._filepath = self.filepath()

    def filepath(self):
        tmp = self._text.lower()
        # print tmp
        chars = "\\`*{}[]()>#+-.!$"
        for c in chars:
            if c in tmp:
                tmp = tmp.replace(c, "")
        # print tmp
        tmp = tmp.replace(" ", "_")
        # print tmp
        tmp = os.path.join(self.FILEDIR, "%s.mp3" % tmp)
        # print tmp
        return tmp

    def _generate_tts_audio(self):
        params = {'key': self.APIKEY,
                  'src': self._text,
                  'hl': self.lang,
                  'c': "MP3",
                  'f': "44khz_16bit_mono",
                  'r': 1
                  }

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            }

        data = urllib.urlencode(params)
        logger.info("Calling TTS API: '%s'" % self.TTS_URL)
        logger.info("  headers: %s" % headers)
        logger.info("  params: %s" % params)
        req = urllib2.Request(self.TTS_URL, data, headers)
        try:
            handle = urllib2.urlopen(req)
        except urllib2.URLError, e:
            raise Exception('ERROR: TTS server not reachable ! (%s)' % e.reason)
        except urllib2.HTTPError, e:
            raise Exception('ERROR: TTS server fails ! (%s)' % e.code)
        else:
            audio_data = handle.read()
            if not audio_data.startswith("ID3"):
                raise Exception('ERROR: TTS returns invalid data: %s' % audio_data)
            print " > returns %d octets" % len(audio_data)
        return audio_data

    def generateMP3(self, filepath=None, force=False):
        if filepath is None: filepath = self._filepath
        """ Do the Web request and save to `savefile` """
        if not os.path.isfile(filepath) or force == True:
            logger.info("Saving speech in '%s'" % filepath)
            with open(filepath, 'wb') as f:
                audio_data = self._generate_tts_audio()
                f.write(audio_data)
        else:
            logger.info("Speech already exists: %s" % filepath)
        return filepath

    def get_mp3_data(self):
        raw_data = ""
        with open(self._filepath, 'rb') as f:
            raw_data = f.read()
        return base64.b64encode(raw_data)

class AudioPlayer:
    def __init__(self, tmp_dir="/tmp/voiceRSS/play"):
        self.FILEDIR = tmp_dir
        if not os.path.isdir(self.FILEDIR):
            os.makedirs(self.FILEDIR)

    def create_mp3file(self, content, filename=None):
        if filename is None: filename = dt.datetime.now().isoformat()+".mp3"
        filepath = os.path.join(self.FILEDIR, filename)
        logger.info("Saving MP3 file in '%s'" % filepath)
        raw_data = base64.b64decode(content)
        with open(filepath, 'wb') as f:
            f.write(raw_data)
        return filepath

    def playfile(self, filepath):
        if not os.path.isfile(filepath):
            logger.error("Audio Player: file '%s' does not exist"%filepath)
            return

        try:
            logger.info("Playing file: %s" % filepath)
            exec_process("/usr/bin/mplayer \"%s\"" % filepath)
        except Exception as e:
            logger.error("Error while playing file: %s" % filepath)

        os.remove(filepath)



######################################################################################
if __name__ == '__main__':
    text = " ".join(sys.argv[1:])
    tts = TextToSpeech(text)
    tts.play()

    exit(0)
