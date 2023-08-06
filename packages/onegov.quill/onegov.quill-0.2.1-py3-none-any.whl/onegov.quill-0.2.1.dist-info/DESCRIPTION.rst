

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Quill follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Onegov Quill uses `Semantic Versioning <http://semver.org/>`_

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.quill.png
  :target: https://travis-ci.org/OneGov/onegov.quill
  :alt: Build Status

Coverage
--------

.. image:: https://coveralls.io/repos/OneGov/onegov.quill/badge.png?branch=master
  :target: https://coveralls.io/r/OneGov/onegov.quill?branch=master
  :alt: Project Coverage

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.quill.svg
    :target: https://badge.fury.io/py/onegov.quill
    :alt: Latest PyPI Release

License
-------
onegov.quill is released under GPLv2

Changelog
---------
0.2.1 (2017-09-29)
~~~~~~~~~~~~~~~~~~~~~

- Adds compatibility with bleach 2.1.
  [msom]

0.2.0 (2017-09-05)
~~~~~~~~~~~~~~~~~~~~~

- Allows to configure the used formats.
  [msom]

- Removes jQuery dependency.
  [msom]

0.1.2 (2017-09-04)
~~~~~~~~~~~~~~~~~~~~~

- Uses Quill 1.3.2.
  [msom]

0.1.1 (2017-09-01)
~~~~~~~~~~~~~~~~~~~~~
- Nothing.
  [msom]

0.1.0 (2017-09-01)
~~~~~~~~~~~~~~~~~~~~~

- Makes toolbar smaller.
  [msom]

0.0.1 (2017-08-31)
~~~~~~~~~~~~~~~~~~~~~

- Initial Release


