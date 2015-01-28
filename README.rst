spyder-coverage-plugin
======================

A Spyder plugin for Ned Batchelder's coverage_ package.

Installation
------------

1.  Put ``p_coverage.py`` in
    ``%pythonpath%\Lib\site-packages\spyderplugins``
2.  Put ``coveragegui.py`` in
    ``%pythonpath%\Lib\site-packages\spyderplugins\widgets``
3.  Load up Spyder. It *should* work.

Usage
-----

With the file open that you want to run coverage on, press
``ALT`` + ``F11``.

Requires
--------

1.  Obviously the ``coverage`` package available on
    PyPI_ with documentation at Ned's website_.
2.  It's a plugin for Spyder, so... you need Spyder_. I've tested it with
    Spyder 2.3.2 and Python 2.7.6. Additional testing is appreciated.


.. _coverage: http://nedbatchelder.com/code/coverage/
.. _PyPI: https://pypi.python.org/pypi/coverage
.. _website: http://nedbatchelder.com/code/coverage/
.. _Spyder: https://code.google.com/p/spyderlib/
