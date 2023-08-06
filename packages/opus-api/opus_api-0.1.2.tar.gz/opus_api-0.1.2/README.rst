::

              /$$$$$$            /$$$$$$$  /$$   /$$  /$$$$$$
             /$$__  $$          | $$__  $$| $$  | $$ /$$__  $$
    /$$$$$$$| $$  \ $$  /$$$$$$ | $$  \ $$| $$  | $$| $$  \__/
   /$$_____/| $$  | $$ /$$__  $$| $$$$$$$/| $$  | $$|  $$$$$$
  | $$      | $$  | $$| $$  \__/| $$____/ | $$  | $$ \____  $$
  | $$      | $$  | $$| $$      | $$      | $$  | $$ /$$  \ $$
  |  $$$$$$$|  $$$$$$/| $$      | $$      |  $$$$$$/|  $$$$$$/
   \_______/ \______/ |__/      |__/       \______/  \______/

.. image:: https://img.shields.io/pypi/v/opus-api.svg
        :target: https://pypi.python.org/pypi/opus-api

.. image:: https://img.shields.io/travis/yonkornilov/opus-api.svg
        :target: https://travis-ci.org/yonkornilov/opus-api

.. image:: https://readthedocs.org/projects/opus-api/badge/
        :target: http://opus-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/yonkornilov/opus-api/shield.svg
        :target: https://pyup.io/repos/github/yonkornilov/opus-api/
        :alt: Updates

.. _OPUS: http://opus.lingfil.uu.se/

OPUS_ (opus.lingfil.uu.se) Python API

* Free software: MIT license
* Documentation: https://opus-api.readthedocs.io.

Features
--------

* Get parallel corpora for src-target languages from OPUS_, the online parallel corpus
* JSON API
* Caching for quick results
* Command Line Interface
* Filter corpora by range of desired total tokens

Usage
_____

Find your languages:

::

  $ opus_api langs

  [
  ...
    {
      "description": "en (English)", 
      "id": 69, 
      "name": "en"
    },
    ...
    {
      "description": "ru (Russian)", 
      "id": 198, 
      "name": "ru"
    }...
  ]

Find corpora:

::

  $ opus_api get en ru --maximum 300 --minimum 3

  {
    "corpora": [
      {
        "id": 1, 
        "name": "OpenSubtitles2016", 
        "src_tokens": "157.5M", 
        "trg_tokens": "133.6M", 
        "url": "http://opus.lingfil.uu.se/download.php?f=OpenSubtitles2016%2Fen-ru.txt.zip"
      },
    ...
      {
        "id": 13, 
        "name": "KDE4", 
        "src_tokens": "1.8M", 
        "trg_tokens": "1.4M", 
        "url": "http://opus.lingfil.uu.se/download.php?f=KDE4%2Fen-ru.txt.zip"
      }
    ]
  }

Credits
---------


.. _click: https://github.com/pallets/click

This package's CLI is powered by click_.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
