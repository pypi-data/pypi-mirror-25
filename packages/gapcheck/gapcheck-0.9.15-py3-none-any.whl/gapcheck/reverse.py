# -*- coding: utf-8 -*-

import os
import glob

from gapcheck import tags
from gapcheck import log


def is_music(name, extension):
    """ Indica si un fichero es música """

    for e in extension:
        if name.endswith('.' + e):
            return True
    return False


def is_music_dir(path, extension):
    """ Comprueba si en el directorio hay ficheros de música """

    for fname in os.listdir(path):
        if is_music(fname, [extension]):
            return True
    return False


def reverse(options):
    reversalize(options.path, options.extension)
    for root, subfolders, files in os.walk(options.path):
        path = root.split(os.sep)
        for subfolder in subfolders:
            path = os.path.join(root, subfolder)
            reversalize(path, options.extension)


def reversalize(path, extension):

    lftr = list()
    lftd = list()

    if not os.path.exists(path):
        return

    # 1. miramos si es un directorio de música
    if not is_music_dir(path, extension):
        return

    backupdir = os.path.join(path, '__backup')

    # 2. si no existe el directorio __backup también salimos
    if not os.path.exists(backupdir):
        return

    # 3. movemos los ficheros de __backup a '.' y los renombramos
    ftr = glob.glob('{}/*.{}{}'.format(backupdir, extension, '_bck'))

    for f in ftr:
        nf = '{}.{}'.format(os.path.splitext(f)[0], extension)
        dst = os.path.join(path, os.path.basename(nf).replace('__BACKUP_', ''))
        lftr.append([os.path.basename(f), os.path.basename(dst)])
        os.rename(f, dst)

    # 4. revisar los ficheros que eran GAPLESS y se juntaron y borrarlos

    ftd = glob.glob('{}/*.{}'.format(path, extension))

    for f in ftd:
        # faudio = os.path.join(path, f)
        if tags.tag_in_file(f, 'gapless_join'):
            lftd.append(os.path.basename(f))
            os.remove(f)

    # 5. si todo va bien, ya podríamos borrar el directori de __backup
    os.removedirs(backupdir)

    log.write_log_reverse(path, extension, lftr, lftd)
