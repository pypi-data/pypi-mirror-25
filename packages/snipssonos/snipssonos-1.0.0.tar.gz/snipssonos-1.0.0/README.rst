Sonos skill for Snips
=====================

|Build Status| |PyPI| |MIT License|


Installation
------------

The skill is on `PyPI <https://pypi.python.org/pypi/snipshue>`_, so you can just install it with `pip <http://www.pip-installer.org>`_:

.. code-block:: console

    $ pip install snipssonos

Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    assistant_id: YOUR_CONSOLE_ASSISTANT_ID
    skills:
      - pip: https://github.com/snipsco/snips-skills-sonos
        package_name: snipssonos
        class_name: SnipsSonos
        params:
          spotify_client_id: YOUR_SPOTIFY_CLIENT_ID
          spotify_client_secret: YOUR_SPOTIFY_CLIENT_SECRET
          spotify_refresh_token: YOUR_SPOTIFY_REFRESH_TOKEN      

Usage
-----

The skill allows you to control `Sonos <http://musicpartners.sonos.com/docs?q=node/442>`_ speakers. In order to use it, you need the IP address of your Hue Bridge, as well as the username:

.. code-block:: python

    from snipssonos.snipssonos import SnipsSonos

    sonos = SnipsSonos(spotify_client_id, spotify_client_secret, spotify_refresh_token)
    sonos.play_artist("John Coltrane")

Copyright
---------

This skill is provided by `Snips <https://www.snips.ai>`_ as Open Source software. See `LICENSE.txt <https://github.com/snipsco/snips-skill-hue/blob/master/LICENSE.txt>`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skill-sonos.svg
   :target: https://travis-ci.org/snipsco/snips-skill-sonos
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipssonos.svg
   :target: https://pypi.python.org/pypi/snipssonos
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-hue/master/LICENSE.txt
   :alt: MIT License
