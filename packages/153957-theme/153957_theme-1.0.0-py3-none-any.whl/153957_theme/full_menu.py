""" Add full menu to gallery

Limitations:
- Currently only supports sorting albums by name in normal order (can not be reversed).

"""

import os
import operator
from collections import OrderedDict

from sigal import signals


def full_tree(gallery):
    """full menu tree"""

    sorted_tree = sorted(gallery.albums.items(), key=operator.itemgetter(0))

    gallery.full_tree = OrderedDict()

    for name, album in sorted_tree:
        if name == '.':
            continue
        ancestors = album.path.split('/')[:-1]
        current_ancestor = gallery.full_tree
        for ancestor in ancestors:
            current_ancestor = current_ancestor[ancestor]['subalbums']
        current_ancestor[album.name] = {
            'self': album,
            'subalbums': OrderedDict()
        }


def path_to_root(album):
    """url path back to gallery root"""

    path_to_root = os.path.relpath('.', album.path)
    if path_to_root == '.':
        path_to_root = ''
    else:
        path_to_root += '/'

    album.path_to_root = path_to_root


def path_from_root(album):
    """url from gallery root"""

    album.path_from_root = album.path


def register(settings):
    signals.gallery_initialized.connect(full_tree)
    signals.album_initialized.connect(path_to_root)
    signals.album_initialized.connect(path_from_root)
