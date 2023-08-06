.. write readme in RestructuredText, MarkDown is not supported by Pypi

===============================
txwebbackendbase
===============================

.. image:: https://travis-ci.org/Stibbons/txwebbackendbase.svg?branch=master
    :target: https://travis-ci.org/Stibbons/txwebbackendbase
.. image:: https://readthedocs.org/projects/txwebbackendbase/badge/?version=latest
   :target: http://txwebbackendbase.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/Stibbons/txwebbackendbase/badge.svg
   :target: https://coveralls.io/github/Stibbons/txwebbackendbase
.. image:: https://badge.fury.io/py/txwebbackendbase.svg
   :target: https://pypi.python.org/pypi/txwebbackendbase/
   :alt: Pypi package
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

Generic Base framework for Web App backend using Twisted

* Free software: MIT
* Documentation: https://txwebbackendbase.readthedocs.org/en/latest/
* Source: https://github.com/Stibbons/txwebbackendbase

Features
--------

* TODO

Usage
-----

* TODO


Note: See `pipenv documentation <https://github.com/kennethreitz/pipenv>`_ for Pipfile
specification.

Contributing
------------

Create your environment with

    .. code-block:: bash

        $ make dev

Activate the environment:

    .. code-block:: bash

        $ make shell

Execute a command directly inside the environment:

    .. code-block:: bash

        $ make run

Execute unit tests:

    .. code-block:: bash

        $ make test-unit

Build source package:

    Use it for most package without low level system dependencies.

    .. code-block:: bash

        make pypi

Build binary package:

    Needed for package with a C or other low level source code.

    .. code-block:: bash

        make bdist

Build Wheel package:

    Always provide a wheel package.

    .. code-block:: bash

        make wheel

(Only for package owner)

Create a release:

    Go on GitHub and create a tag with a semver syntax. Optionally you can tag code locally and push
    to GitHub.

    .. code-block:: bash

        git tag 1.2.3
        make push

    On successful travis build on the Tag branch, your Pypi package will be updated automatically.
