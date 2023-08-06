pycent
======

pycent is a simple module to quickly return the percentage of a value,
or the reverse.

Usage
-----

::

    >>> from pycent import pycent
    >>> pycent().percentage(1,2)
    0.5
    >>> pycent().percentage(5, 19, 3)
    26.316
    >>> pycent().percent_of(5, 20)
    1.0