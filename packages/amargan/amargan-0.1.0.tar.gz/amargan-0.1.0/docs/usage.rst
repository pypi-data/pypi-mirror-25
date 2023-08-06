=====
Usage
=====

Programmatic
------------

Amargan takes any iterable that yields strings, thus making it memory efficient:

*Example: From the contents of a file*

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... with open(filename) as fp:
    ...     anagrams = Amargan(fp.readlines())
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])
    ... anagrams.for_word('abc')
    set(['abc', 'acb', 'cba'])

*Example: From an open file*

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... with open(filename) as fp:
    ...     anagrams = Amargan(fp)
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])
    ... anagrams.for_word('abc')
    set(['abc', 'acb', 'cba'])

*Example: From a StringIO*

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... sio = six.StringIO(buf='cba\nabc\nacb\n')
    ... anagrams = Amargan(sio)
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])
    ... anagrams.for_word('abc')
    set(['abc', 'acb', 'cba'])

*Example: From a list*

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... anagrams = Amargan(['cba', 'abc', 'acb'])
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])
    ... anagrams.for_word('abc')
    set(['abc', 'acb', 'cba'])



There are configurable `Iterators` to allow you to read from a file using a non-default
configuration.

For example, to iterate over a multi-line file containing words separated by a comma:

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan, Iterator, IteratorType
    ...
    ... with open(filename) as fp:
    ...     iterator = Iterator(IteratorType.multi_per_line, sep=',')
    ...     anagrams = Amargan(iterator(fp))
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])


To iterate over a multi-line file containing lines of one or more words separated by a whitespace
(the default iterator configuration):

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... with open(filename) as iterator:
    ...     anagrams = Amargan(iterator)
    ... anagrams['abc']
    set(['abc', 'acb', 'cba'])

Add and remove words from the dictionary:

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... anagrams = Amargan()
    ... anagrams['acb']
    frozenset()
    ... anagrams += 'abc acb cab'
    ... anagrams['acb']
    set(['abc', 'acb', 'cba'])
    ... anagrams -= 'acb'
    ... anagrams['acb']
    set(['abc', 'cba'])

.. code-block:: python
    :linenos:

    >>> from amargan import Amargan
    ...
    ... anagrams = Amargan()
    ... anagrams['acb']
    frozenset()
    ... x = anagrams + 'abc acb cab'
    ... x
    Amargan(True - 1)
    ... x['acb']
    set(['abc', 'acb', 'cba'])
    ... x = anagrams - 'acb'
    ... x['acb']
    set(['abc', 'cba'])

Command-line
------------

To use amargan from the command-line for single words
(anagrams are ordered and contain the original word by default):

.. code-block:: bash
    :linenos:

    $ find_anagrams -i words.txt hello
    elloh hello lehol


and for multiple words:

.. code-block:: bash
    :linenos:

    $ find_anagrams --ip=words.txt hello world
    elloh hello lehol
    lordw rlwdo world


and with options:

.. code-block:: bash
    :linenos:

    $ find_anagrams --exclude --output-iterator=one_per_line --case-sensitive --ip=words.txt Hello
    elloH
    leHol

