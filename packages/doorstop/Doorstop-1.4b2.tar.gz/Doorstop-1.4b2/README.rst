| |Build Status|
| |Coverage Status|
| |Scrutinizer Code Quality|
| |PyPI Version|
| |Best Practices|

Overview
========

Doorstop is a `requirements
management <http://alternativeto.net/software/doorstop/>`__ tool that
facilitates the storage of textual requirements alongside source code in
version control.

When a project utilizes this tool, each linkable item (requirement, test
case, etc.) is stored as a YAML file in a designated directory. The
items in each directory form a document. The relationship between
documents forms a tree hierarchy. Doorstop provides mechanisms for
modifying this tree, validating item traceability, and publishing
documents in several formats.

Doorstop is under active development and we welcome contributions.

The project is licensed as GPLv3.

To report a problem or a security vulnerability please raise an
`issue <https://github.com/jacebrowning/doorstop/issues>`__

Additional reading:

-  publication: `JSEA
   Paper <http://www.scirp.org/journal/PaperInformation.aspx?PaperID=44268#.UzYtfWRdXEZ>`__
-  talks:
   `GRDevDay <https://speakerdeck.com/jacebrowning/doorstop-requirements-management-using-python-and-version-control>`__,
   `BarCamp <https://speakerdeck.com/jacebrowning/strip-searched-a-rough-introduction-to-requirements-management>`__
-  sample: `Generated
   HTML <http://jacebrowning.github.io/doorstop/index.html>`__

Setup
=====

Requirements
------------

-  Python 3.3+
-  A version control system for requirements storage

Installation
------------

Install Doorstop with pip:

.. code:: sh

    $ pip install doorstop

or directly from source:

.. code:: sh

    $ git clone https://github.com/jacebrowning/doorstop.git
    $ cd doorstop
    $ python setup.py install

After installation, Doorstop is available on the command-line:

.. code:: sh

    $ doorstop --help

And the package is available under the name 'doorstop':

.. code:: sh

    $ python
    >>> import doorstop
    >>> doorstop.__version__

Usage
=====

Switch to an existing version control working directory, or create one:

.. code:: sh

    $ git init .

Create documents
----------------

Create a new parent requirements document:

.. code:: sh

    $ doorstop create SRD ./reqs/srd

Add a few items to that document:

.. code:: sh

    $ doorstop add SRD
    $ doorstop add SRD
    $ doorstop add SRD

Link items
----------

Create a child document to link to the parent:

.. code:: sh

    $ doorstop create HLTC ./tests/hl --parent SRD
    $ doorstop add HLTC

Link items between documents:

.. code:: sh

    $ doorstop link HLTC001 SRD002

Publish reports
---------------

Run integrity checks on the document tree:

.. code:: sh

    $ doorstop

Publish the documents as HTML:

.. code:: sh

    $ doorstop publish all ./public

.. |Build Status| image:: http://img.shields.io/travis/jacebrowning/doorstop/master.svg
   :target: https://travis-ci.org/jacebrowning/doorstop
.. |Coverage Status| image:: http://img.shields.io/coveralls/jacebrowning/doorstop/master.svg
   :target: https://coveralls.io/r/jacebrowning/doorstop
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/jacebrowning/doorstop.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/doorstop/?branch=master
.. |PyPI Version| image:: http://img.shields.io/pypi/v/Doorstop.svg
   :target: https://pypi.python.org/pypi/Doorstop
.. |Best Practices| image:: https://bestpractices.coreinfrastructure.org/projects/754/badge
   :target: https://bestpractices.coreinfrastructure.org/projects/754
