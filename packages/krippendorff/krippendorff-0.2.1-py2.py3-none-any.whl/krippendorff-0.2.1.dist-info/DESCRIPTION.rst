Krippendorff
============

Fast computation of `Krippendorff's
alpha <https://en.wikipedia.org/wiki/Krippendorff%27s_alpha>`__
agreement measure.

Based on `Thomas Grill
implementation <https://github.com/grrrr/krippendorff-alpha>`__. Works
on Python 3+.

Example usage
-------------

Given a reliability data matrix, run:

.. code:: python

    import krippendorff

    krippendorff.alpha(reliability_data)

See ``sample.py`` and ``alpha`` docstring for more.

Installation
------------

.. code:: shell

    pip install krippendorff

Caveats
-------

The implementation is fast as it doesn't do a nested loop for the
coders. However, V should be small, since a matrix of VxV it's used.


