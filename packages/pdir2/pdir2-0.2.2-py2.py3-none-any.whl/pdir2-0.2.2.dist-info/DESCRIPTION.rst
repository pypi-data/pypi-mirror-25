pdir2: Pretty dir() printing with joy
=====================================

|Build Status| |Supported Python versions| |PyPI Version|

Have you ever dreamed of a better output of ``dir()``? I do. So I
created this.

.. figure:: https://github.com/laike9m/pdir2/raw/master/images/presentation_v2.gif
   :alt: 

Features
--------

-  Attributes are grouped by types/functionalities, with beautiful
   colors.

-  Support color customization, `here's
   how <https://github.com/laike9m/pdir2/wiki/User-Configuration>`__.

-  Support all platforms including Windows(Thanks to
   `colorama <https://github.com/tartley/colorama>`__).

-  Support `ipython <https://github.com/ipython/ipython>`__,
   `ptpython <https://github.com/jonathanslenders/ptpython>`__,
   `bpython <https://www.bpython-interpreter.org/>`__ and `Jupyter
   Notebook <http://jupyter.org/>`__! See
   `wiki <https://github.com/laike9m/pdir2/wiki/REPL-Support>`__ for
   details.

-  The return value of ``pdir()`` can still be used as a list of names.

-  You can search for certain names with ``.s()`` or ``.search()``:

.. figure:: https://github.com/laike9m/pdir2/raw/master/images/search.gif
   :alt: 

| Search is case-insensitive by default.
| You can use ``.search(name, case_sensitive=True)`` to do case
  sensitive searching.

Install
-------

::

    pip install pdir2

About the name. I wanted to call it "pdir", but there's already one with
this name on pypi. Mine is better, of course.

As a better alternative of ``dir()``, it's more convenient to
automatically import pdir2 when launching REPL. Luckily, Python provides
a way to do this. In you ``.bashrc``\ (or ``.zshrc``), add this line:

::

    export PYTHONSTARTUP=$HOME/.pythonstartup

Then, create ``.pythonstartup`` in your home folder. Add one line:

::

    import pdir

Next time you launch REPL, ``pdir()`` is already there, Hooray!

Testing
-------

Simply run ``pytest``, or use ``tox`` if you like.

.. |Build Status| image:: https://travis-ci.org/laike9m/pdir2.svg
   :target: https://travis-ci.org/laike9m/pdir2
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/pdir2.svg
   :target: https://pypi.python.org/pypi/pdir2/
.. |PyPI Version| image:: https://img.shields.io/pypi/v/pdir2.svg



Release History
===============

0.2.0(2017-04-04)
-----------------

-  Add support for color customization. (#14)

0.1.0(2017-03-16)
-----------------

-  Add support for ipython, ptpython and bpython (#4)

0.0.2(2017-03-11)
-----------------

API Changes (Backward-Compatible)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Added a ``case_sensitive`` parameter into the ``search`` function
   (#5)

Bugfixes
~~~~~~~~

-  Error calling pdir(pandas.DataFrame) (#1)
-  Methods are now considered functions (#6)


