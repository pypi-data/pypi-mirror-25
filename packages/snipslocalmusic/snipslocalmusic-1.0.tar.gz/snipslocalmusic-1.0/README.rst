Local music player skill for Snips
==================================

|Build Status| |PyPI| |MIT License|


Installation
------------

The skill is on `PyPI`_, so you can just install it with `pip`_:

.. code-block:: console

    $ pip install snipslocalmusic

Snips Skills Manager
^^^^^^^^^^^^^^^^^^^^

It is recommended that you use this skill with the `Snips Skills Manager <https://github.com/snipsco/snipsskills>`_. Simply add the following section to your `Snipsfile <https://github.com/snipsco/snipsskills/wiki/The-Snipsfile>`_:

.. code-block:: yaml

    skills:
    - package_name: snipslocalmusic
      class_name: SnipsLocalMusic
      pip: snipslocalmusic
      params:
        db_file_path: data/music/db.json



Usage
-----

The skill allows you to play music using local files.

.. code-block:: python

    from snipslocalmusic.snipslocalmusic import SnipsLocalMusic

    music = SnipsLocalMusic("db.json") 
    music.play(None, None, None, "Bach")

Here is how the `db.json`_ file should be formatted : 
.. code-block:: json
	{
    		"songs": [
        		{	
            			"artist": "Bach",
            			"title": "Air",
            			"genres": ["classical"],
            			"playlists": ["work"],
            			"filename": "data/music/files/Bach-Air.mp3"
        		}, 
    		]
	}


Copyright
---------

This skill is provided by `Snips`_ as Open Source software. See `LICENSE.txt`_ for more
information.

.. |Build Status| image:: https://travis-ci.org/snipsco/snips-skill-localmusic.svg
   :target: https://travis-ci.org/snipsco/snips-skill-localmusic
   :alt: Build Status
.. |PyPI| image:: https://img.shields.io/pypi/v/snipslocalmusic.svg
   :target: https://pypi.python.org/pypi/snipslocalmusic
   :alt: PyPI
.. |MIT License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/snipsco/snips-skill-localmusic/master/LICENSE.txt
   :alt: MIT License

.. _`PyPI`: https://pypi.python.org/pypi/snipshue
.. _`pip`: http://www.pip-installer.org
.. _`Snips`: https://www.snips.ai
.. _`LICENSE.txt`: https://github.com/snipsco/snips-skill-smartercoffee/blob/master/LICENSE.txt
