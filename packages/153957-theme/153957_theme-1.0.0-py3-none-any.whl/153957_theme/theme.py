""" Use the 153957-theme as theme for the gallery
"""

import os

from sigal import signals


def theme(gallery):
    """set theme settings to this theme"""

    theme_directory = os.path.dirname(os.path.abspath(__file__))
    gallery.settings['theme'] = theme_directory


def register(settings):
    signals.gallery_initialized.connect(theme)
