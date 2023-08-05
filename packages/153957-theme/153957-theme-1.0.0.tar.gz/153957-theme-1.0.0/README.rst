153957 theme
============

.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/153957/153957-theme/blob/master/LICENSE
.. image:: http://img.shields.io/travis/153957/153957-theme/master.svg
   :target: https://travis-ci.org/153957/153957-theme


`View demo album here <https://153957.github.io/153957-theme/>`_


Photo gallery template
----------------------

Web photo gallery templates adapted to my personal preferences.


Usage
-----

This section describes how to install an use this theme.

Installation
~~~~~~~~~~~~

Install the ``153597_theme`` package::

    $ pip install git+https://github.com/153957/153957-theme.git@master#egg=153957-theme


Configure
~~~~~~~~~

In the ``sigal.conf.py`` of an album the ``theme`` setting should normally be
set to either one of the themes included in ``sigal`` or the path to a theme.
However, since the theme is included in this package its location might be
difficult to determine. In order simplify this a plugin is included which sets
the theme automatically when the ``Gallery`` is initialized.

Set ``theme`` to an empty string and add the theme and menu plugins::

    theme = ''
    plugins = ['153957_theme.theme', '153957_theme.full_menu', …]


Sources
-------

Based on `sigal <http://sigal.saimon.org/>`_ version of Galleria theme, which is
distributed under the MIT License.

Theme based on `Galleria Classic <http://galleria.io/>`_, which is distributed under
the MIT License.
