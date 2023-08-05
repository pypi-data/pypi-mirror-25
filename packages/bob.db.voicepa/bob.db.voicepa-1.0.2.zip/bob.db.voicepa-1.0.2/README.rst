.. vim: set fileencoding=utf-8 :
.. Mon Oct 10 22:06:22 CEST 2016

.. image:: http://img.shields.io/badge/docs-v1.0.2-yellow.png
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.voicepa/v1.0.2/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.db.voicepa/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.voicepa/badges/v1.0.2/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voicepa/commits/v1.0.2
.. image:: https://gitlab.idiap.ch/bob/bob.db.voicepa/badges/v1.0.2/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voicepa/commits/v1.0.2
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.voicepa
.. image:: http://img.shields.io/pypi/v/bob.db.voicepa.png
   :target: https://pypi.python.org/pypi/bob.db.voicepa


====================================
 voicePA Database Interface for Bob
====================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains the access API and descriptions for the voicePA_ Database.
The database focuses on speech presentation attacks. For the genuine data, it
contains speech recordings from AVspoof_, which include speech from 44 persons
(31 males and 13 females) performed during the course of two months in four
different sessions.

The database contains large number of different presentation attacks, obtained
by replaying different type of speech, including recorded speech, voice
conversion, and speech synthesis, to microphones of different devices (laptop,
iPhone 3GS, and Samsung S3) using different speakers (high quality speakers,
laptop, iPhone 6S, iPhone 3GS, and Samsung S3) and in different environments
(two office rooms and a conference room).

This package contains the Bob_-compliant interface implementation with methods
to use the database directly from Python with provided protocols.


Installation
------------

Complete Bob's `installation`_ instructions. Then, to install this package,
run::

  $ conda install bob.db.voicepa


Contact
-------

For questions or reporting issues to this software package, contact our
devopment `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-dev
.. _voicePA: https://www.idiap.ch/dataset/voicepa
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
