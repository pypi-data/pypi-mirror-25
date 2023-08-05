# -*- coding: utf-8 -*-

import unittest
import sys
import os
import pathlib
import shutil
from mutagen.flac import FLAC
from gapcheck import join
from gapcheck import log
from gapcheck import gap
from gapcheck import reverse
from gapcheck import buildparser


class TestReverse(unittest.TestCase):
    """ Test Reverse """

    def setUp(self):
        """ Limpieza y generación de ficheros necesarios """
        # limpieza por si hubiera ficheros mal

        dir_to_create = ['./tests/audio/reverse/__backup']

        for dtc in dir_to_create:
            if not os.path.exists(dtc):
                os.makedirs(dtc)

        files_to_delete = []

        for ftd in files_to_delete:
            if os.path.isfile(ftd):
                os.remove(ftd)

        f2mv = [['./tests/audio/reverse/01-gap.flac',
                 './tests/audio/reverse/__backup/__BACKUP_01-gap.flac_bck'],
                ['./tests/audio/reverse/02-silence.flac',
                 './tests/audio/reverse/__backup/__BACKUP_02-silence.flac_bck'],
                ['./tests/audio/reverse/03-gap.flac',
                 './tests/audio/reverse/__backup/__BACKUP_03-gap.flac_bck'],
                ['./tests/audio/reverse/04-gap.flac',
                 './tests/audio/reverse/__backup/__BACKUP_04-gap.flac_bck'],
                ['./tests/audio/reverse/05-silence.flac',
                 './tests/audio/reverse/__backup/__BACKUP_05-silence.flac_bck']]

        for ftr in f2mv:
            if os.path.isfile(ftr[0]):
                os.rename(ftr[0], ftr[1])

        dirs_to_delete = []

        for dtd in dirs_to_delete:
            if os.path.isdir(dtd):
                shutil.rmtree(dtd)

        f2cp = [['./tests/audio/back/01-gap__GAPLESS.flac',
                 './tests/audio/reverse/01-gap__GAPLESS.flac'],
                ['./tests/audio/back/03-gap__GAPLESS.flac',
                 './tests/audio/reverse/03-gap__GAPLESS.flac']]

        for ftc in f2cp:
            if os.path.isfile(ftc[0]):
                shutil.copy(ftc[0], ftc[1])

    def test_log_reverse(self):
        """ Test de generacion de log """

        path = './tests/audio/reverse'
        extension = 'flac'
        ftr = ['./tests/audio/reverse/__backup/__BACKUP_01-gap.flac_bck',
               './tests/audio/reverse/__backup/__BACKUP_02-silence.flac_bck']
        ftd = ['./tests/audio/reverse/01-gap__GAPLESS.flac']

        loginfo = log.gen_loginfo_reverse(path, extension, ftr, ftd)
        self.assertEqual(loginfo['reverse_dir'], './tests/audio/reverse')
        self.assertEqual(loginfo['extension'], 'flac')
        self.assertEqual(loginfo['files_restored'], ftr)
        self.assertEqual(loginfo['files_deleted'], ftd)

    def test_argparser_reverse(self):
        """ Test de parametros """

        parser = buildparser.build_parser()

        options = parser.parse_args(['-r'])
        self.assertTrue(options.reverse)

        options = parser.parse_args([])
        self.assertFalse(options.reverse)

    def test_reverse(self):
        """ Prueba completa con reverse """

        # No es posible testear el directorio
        expected = ['reverse_dir: null',
                    'extension: flac',
                    'files_restored: 5',
                    ' - __BACKUP_01-gap.flac_bck -> 01-gap.flac',
                    ' - __BACKUP_02-silence.flac_bck -> 02-silence.flac',
                    ' - __BACKUP_03-gap.flac_bck -> 03-gap.flac',
                    ' - __BACKUP_04-gap.flac_bck -> 04-gap.flac',
                    ' - __BACKUP_05-silence.flac_bck -> 05-silence.flac',
                    'files_deleted: 2',
                    ' - 01-gap__GAPLESS.flac',
                    ' - 03-gap__GAPLESS.flac']

        parser = buildparser.build_parser()
        options = parser.parse_args(['-r', '-p', './tests/audio/reverse'])

        reverse.reverse(options)

        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        # because stdout is an StringIO instance
        output = sys.stdout.getvalue().strip().replace('\\', '/').split('\n')

        for i in range(len(output)):
            if 'reverse_dir' in output[i]:
                continue
            else:
                self.assertEqual(output[i], expected[i])

        # TODO: revisar los ficheros resultantes
