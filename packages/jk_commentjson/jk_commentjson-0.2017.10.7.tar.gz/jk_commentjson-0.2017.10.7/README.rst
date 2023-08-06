jk_commentjson
==============

Introduction
------------

This python module allows reading JSON files including comments.

This module is an improved version of Vaidik Kapoor's ``commentjson`` module provided at PyPi at ``https://pypi.python.org/pypi/commentjson/``. The original version has been ported to Python 3 and the regular expressions have been improved.

Information about this module can be found here:

* github.org_
* pypi.python.org_

.. _github.org: https://github.com/jkpubsrc/python-module-jk-commentjson
.. _pypi.python.org: https://pypi.python.org/pypi/jk_commentjson

Foreword
--------

The original ``commentjson`` module implemented by Vaidik Kapoor makes use of regular expressions to preprocess files before forwarding the data to the Python ``json`` parser to actually parse the data. Of course this approach must be considered to be a hack, especially as the existing implementation does not manage all special situations in parsing.

The library `jk_commentjson` improves on the current implementation by fixing and extending the expression approach. Though the current approach works quite well nevertheless it is still a hack.

The author of `jk_commentjson` will replace the existing implementation with a real parser one day, but that will take a bit of time to fully implement and test. Unfortunately due to lack of time this can't be done in the next weeks or months. Besides: The current approach works well in most use cases anyway. Till that day until the existing implementation will be replaced all users of this library will need to get along with the current implementation. Which you will likely find working pretty well until you not run into the following bug:

* If a JSON file is provided in a single line not terminated by a line feed, comments in this file will not be parsed.

So use multi-line JSON files please (which you will likely do anyway as comments in JSON files indicate that these files address human beings and therefor will not be single-line-JSON files anyway).

How to use this module
----------------------

### Import

To import this module use the following statement:

::

  import jk_commentjson

### Parsing

You can parse JSON files like this:

::

  json_loaded = commentjson.loads(json_string)

A JSON file can contain comments of the following style:

* line comments using "//" (C-style comments)
* line comments using "#" (Python-style comments)

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



