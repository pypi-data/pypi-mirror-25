|language| |license|

=========
regmitter
=========

Description
~~~~~~~~~~~

This utility is designed for transferring docker registries data.

Installation
~~~~~~~~~~~~

``python setup.py install``

or

``pip install -e .``

or

``pip install regmitter``

How to use
~~~~~~~~~~

Run ``regmitter -t pull images.yml``

Example of yml file entry: ``"sample-registry.com:5000/app": ["1.0.0-124"]``

Also checkout list of `arguments`_

arguments
^^^^^^^^^

* ``images`` - Path to the file with images to transfer.
* ``-t, --type`` - Type of the operation. Choose from: ``pull``, ``push``, ``remove``
* ``-l, --log`` - Redirect logging to file

.. |language| image:: https://img.shields.io/badge/language-python-blue.svg
.. |license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg

