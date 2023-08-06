=============
About Amargan
=============

.. image:: https://img.shields.io/badge/Author:%20francis%20horsman-Available-brightgreen.svg?style=plastic
    :target: https://www.linkedin.com/in/francishorsman

.. image:: https://img.shields.io/pypi/v/amargan.svg
    :target: https://pypi.python.org/pypi/amargan
        :alt: PyPi version

.. image:: https://img.shields.io/travis/sys-git/amargan.svg
    :target: https://travis-ci.org/sys-git/amargan
        :alt: CI Status

.. image:: https://coveralls.io/repos/github/sys-git/amargan/badge.svg
    :target: https://coveralls.io/github/sys-git/amargan
        :alt: Coverage Status

.. image:: https://badge.fury.io/py/amargan.svg
    :target: https://badge.fury.io/py/amargan

.. image:: https://img.shields.io/pypi/l/amargan.svg
    :target: https://img.shields.io/pypi/l/amargan.svg

.. image:: https://img.shields.io/pypi/wheel/amargan.svg
    :target: https://img.shields.io/pypi/wheel/amargan.svg

.. image:: https://img.shields.io/pypi/pyversions/amargan.svg
    :target: https://img.shields.io/pypi/pyversions/amargan.svg

.. image:: https://img.shields.io/pypi/status/amargan.svg
    :target: https://img.shields.io/pypi/status/amargan.svg

.. image:: https://readthedocs.org/projects/amargan/badge/?version=latest
    :target: https://amargan.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sys-git/amargan/shield.svg
    :target: https://pyup.io/repos/github/sys-git/amargan/
     :alt: Updates

.. code-block:: python
    :linenos:

    >>> print('Anagrams for everyone')


Reasons to use amargan
----------------------

* A simple but powerful pythonic interface

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... with open('words.txt') as iterator:
    ...     anagrams = Amargan(iterator)
    ... anagrams['hello']
    set(['elloh' 'hello' 'lehol'])

* A powerful command-line tool

.. code-block:: bash
    :linenos:

    $ find_anagrams -i words.txt hello
    elloh hello lehol

    $ amargan -i words.txt hello
    elloh hello lehol

* Extensive configuration options

    - Case (in)sensitivity

    - Exclusion of word from results

    - Output formatting (one per line, multiple-per-line, custom seperator)

    - Output to a file

    - Read from a file

    - Use existing dictionary of words

* Time complexity: O(1)
* Space complexity: O(n)  where n = number of words in dictionary.
* Memory efficient, uses iterators extensively.
* Add and remove word(s) from the dictionary.
* Extensively tested with excellent code and branch coverage.
* Extensive error checking with a rich set of checked exceptions.
* Uses `Certifiable <https://pypi.python.org/pypi/certifiable>`_ if available to catch runtime type and parameter validation errors.
* JSON serializable and reconstitutable.
* Fully documented
* Free software: MIT license
* Documentation: https://amargan.readthedocs.io
