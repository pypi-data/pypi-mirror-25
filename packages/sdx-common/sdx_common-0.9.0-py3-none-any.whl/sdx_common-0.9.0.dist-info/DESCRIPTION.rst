..  Titling
    ##++::==~~--''``

SDX-common
::::::::::

.. image:: https://api.codacy.com/project/badge/Grade/b977b40c85da4c7d9cf1a43ade2135d5
    :target: https://www.codacy.com/app/ons-sdc/sdx-common?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ONSdigital/sdx-common&amp;utm_campaign=Badge_Grade

Common classes for SDX apps. Contains a single package:

    * sdx.common_

sdx.common
==========

A common library for SDX apps. App projects declare their dependence on *sdx-common* which
is deployed and installed via pip.

Basic use
=========

Assuming a Python 3.5 virtual environment at ``~/py3.5``:

#. Run the unit tests::

    ~/py3.5/bin/python -m unittest discover sdx

#. Create a package for deployment::

    ~/py3.5/bin/python setup.py sdist

#. Install source package with pip::

    ~/py3.5/bin/pip install -U dist/sdx-common-x.y.z.tar.gz

#. Install extra dependencies for development and building documentation::

    ~/py3.5/bin/pip install .[dev,docbuild]

#. Build documentation pages::

    ~/py3.5/bin/sphinx-build sdx/common/doc sdx/common/doc/html



