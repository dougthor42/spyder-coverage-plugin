spyder-coverage-plugin
======================

A Spyder plugin for Ned Batchelder's [`coverage`](http://nedbatchelder.com/code/coverage/)
package

Installation
------------

1. Put p_coverage.py in ``%pythonpath%\Lib\site-packages\spyderplugins``
2. Put coveragegui.py in ``%pythonpath%\Lib\site-packages\spyderplugins\widgets``
3. Load up spyder. It *should* work.

Usage
-----

With the file open that you want to run coverage on, press <kbd>ALT</kbd>+<kbd>F11</kbd>.

Requires
--------

1. Obviously the ``coverage`` package available on
   [PyPI](https://pypi.python.org/pypi/coverage) with documentation at Ned's
   [website](http://nedbatchelder.com/code/coverage/).
2. It's a plugin for Spyder, so... you need [Spyder](https://code.google.com/p/spyderlib/). I've
   tested it with Spyder 2.3.2. Additional testing is appreciated.
