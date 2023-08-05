REVERPF
=======

|pypi-version| |License|

Reverse `Printf <http://man.he.net/man3/printf>`__.

I dont understand
-----------------

Look this code (python):

.. code:: python

    >>> print("%2d%2d" % (19, 81))
    1981

Oh well, but what's happen if I need revert the number 1981 to original
19 and 81?:

.. code:: shell

    $ echo "1981" | reverpf "%2d%2d"
    |19|81

Of course, only works in fixed print.

System requirements
-------------------

-  Python3

Compatibility
-------------

I do not know if the printf of C is a standard, but it seems that the
python works the same.

Installation
~~~~~~~~~~~~

.. code:: shell

    $ pip install reverpf

Help
----

Usage
~~~~~

::

    usage: reverpf [-h] -f FORMAT [-i FILE] [-s SEPARATOR] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Format from printf
      -i FILE, --input-file FILE
                            File input
      -s SEPARATOR, --separator SEPARATOR
                            Separator string
      -v, --version         show program's version number and exit

Examples
~~~~~~~~

.. code:: shell

    # From stdin
    $ echo "1981" | reverpf -f "%2d%2d"
    ;19;81;

    # From file
    $ reverpf -f "%2d%2d" -i file.txt -s "|"
    |19|81|

License
-------

MIT

.. |pypi-version| image:: https://img.shields.io/pypi/v/reverpf.svg?style=flat-square
   :target: https://pypi.python.org/pypi?:action=display&name=reverpf&version=0.5.0
.. |License| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: LICENSE


