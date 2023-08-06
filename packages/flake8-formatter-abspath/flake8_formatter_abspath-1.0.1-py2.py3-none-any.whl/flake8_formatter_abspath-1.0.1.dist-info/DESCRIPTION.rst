===============================
flake8-formatter-abspath
===============================


.. image:: https://img.shields.io/pypi/v/flake8_formatter_abspath.svg
        :target: https://pypi.python.org/pypi/flake8_formatter_abspath

.. image:: https://img.shields.io/travis/jarshwah/flake8_formatter_abspath.svg
        :target: https://travis-ci.org/jarshwah/flake8_formatter_abspath

.. image:: https://pyup.io/repos/github/jarshwah/flake8_formatter_abspath/shield.svg
     :target: https://pyup.io/repos/github/jarshwah/flake8_formatter_abspath/
     :alt: Updates


A flake8 formatter plugin that shows the absolute path of files with warnings.

* Free software: MIT license

Installation
------------

.. code-block:: bash

     pip3 install flake8
     pip3 install flake8_formatter_abspath

Usage
-----

.. code-block:: bash

     $ flake8 --format=abspath flake8_formatter_abspath
     /Users/jarshwah/dev/flake8_formatter_abspath/flake8_formatter_abspath/plugin.py:5:1: F401 'sys' imported but unused

Jenkins WarningsPublisher
-------------------------

TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

1.0.1 (2017-10-05)
------------------

* Updated packages
* Added compatibility with flake8 3.4.0+

1.0.0 (2017-04-08)
------------------

* Use `flake8 --format=abspath` to report the absolute path of files with warnings


