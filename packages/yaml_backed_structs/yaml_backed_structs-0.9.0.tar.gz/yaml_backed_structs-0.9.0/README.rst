yaml_backed_structs
===================

.. image:: https://img.shields.io/pypi/v/yaml_backed_structs.svg
    :target: https://pypi.python.org/pypi/yaml_backed_structs
    :alt: Latest PyPI version

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://img.shields.io/github/license/mashape/apistatus
    :alt: License
          
Basic python data structures backed by a human editable yaml file

Description
-----------

Provides a dead simple way to store small amounts of information for python programs.
This is useful for program configs and similar.

Has the advantage that the files backing the data structures are human readable and
can be edited using your favorite text editor.

.. code-block:: python

   from yaml_backed_structs import PersistentDict, PersistentSet

   pdict = PersistentDict('my-path.yml')
   pdict['a'] = 1 # this will automatically be saved
   pdict['b'] = []
   pdict['b'].append(2) # this will not be saved automatically
   pdict.save() # but we can save it like this

   


Installation
------------

.. code-block:: bash
   
   pip install yaml_backed_structs

   python setup.py install

Licence
-------

MIT

Authors
-------

`yaml_backed_structs` was written by `David C. Danko <dcdanko@gmail.com>`_.
