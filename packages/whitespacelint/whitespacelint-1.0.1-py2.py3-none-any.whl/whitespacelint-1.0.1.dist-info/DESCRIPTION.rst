==============================================
whitespacelint - Linting tool for whitespace
==============================================

Simple Linting tool for whitespace written in Python based on [bashlint](https://github.com/skudriashev/bashlint)


Installation
------------
``whitespacelint`` can be installed via the Python Package Index or from source.

Using ``pip`` to install ``whitespacelint``::

    $ pip install whitespacelint

You can download the source tarball and install ``whitespacelint`` as follows::

    $ python setup.py install

or in development mode::

    $ python setup.py develop


Rules list
----------
**W201 Trailing whitespace**: Trailing whitespaces are superfluous::

    Okay: echo Test#
    W201: echo Test #

**W202 Blank line contains whitespace**: Trailing whitespaces on blank lines
are superfluous::

    Okay: #
    W202:  #

**W203 Trailing semicolon**: Trailing semicolons are superfluous::

    Okay: echo Test#
    W203: echo Test;#


