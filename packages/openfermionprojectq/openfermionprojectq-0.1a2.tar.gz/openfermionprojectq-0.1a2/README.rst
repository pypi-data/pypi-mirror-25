OpenFermion-ProjectQ
====================

.. image:: https://travis-ci.org/quantumlib/OpenFermion-ProjectQ.svg?branch=master
    :target: https://travis-ci.org/quantumlib/OpenFermion-ProjectQ

.. image:: https://coveralls.io/repos/github/quantumlib/OpenFermion-ProjectQ/badge.svg?branch=master
    :target: https://coveralls.io/github/quantumlib/OpenFermion-ProjectQ?branch=develop

.. image:: https://badge.fury.io/py/openfermionprojectq.svg
    :target: https://badge.fury.io/py/openfermionprojectq

`OpenFermion <http://openfermion.org>`_ is an open source package for compiling and analyzing quantum algorithms that simulate fermionic systems.
This plugin library allows the circuit simulation and compilation package `ProjectQ <https://projectq.ch>`_ to interface with OpenFermion.

Getting started
---------------

To install the latest development versions of OpenFermion, ProjectQ and OpenFermion-ProjectQ,
clone `this <http://github.com/quantumlib/OpenFermion-ProjectQ>`__ git repo, change directory to the top level folder and run:

.. code-block:: bash

  python -m pip install -e .

Alternatively, if using OpenFermion-ProjectQ as a library, one can install the last official PyPI release with:

.. code-block:: bash

  python -m pip install --pre --user openfermionprojectq

How to contribute
-----------------

We'd love to accept your contributions and patches to OpenFermion-ProjectQ.
There are a few guidelines you need to follow.
Contributions to OpenFermion-ProjectQ must be accompanied by a Contributor License Agreement.
You (or your employer) retain the copyright to your contribution,
this simply gives us permission to use and redistribute your contributions as part of the project.
Head over to https://cla.developers.google.com/
to see your current agreements on file or to sign a new one.

All submissions, including submissions by project members, require review.
We use GitHub pull requests for this purpose. Consult
`GitHub Help <https://help.github.com/articles/about-pull-requests/>`__ for
more information on using pull requests.
Furthermore, please make sure your new code comes with extensive tests!
We use automatic testing to make sure all pull requests pass tests and do not
decrease overall test coverage by too much. Make sure you adhere to our style
guide. Just have a look at our code for clues. We mostly follow
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ and use
the corresponding `linter <https://pypi.python.org/pypi/pep8>`_ to check for it.
Code should always come with documentation.

Authors
-------

`Ryan Babbush <http://ryanbabbush.com>`__ (Google),
`Jarrod McClean <http://jarrodmcclean.com>`__ (Google),
`Ian Kivlichan <http://aspuru.chem.harvard.edu/ian-kivlichan/>`__ (Harvard),
Damian Steiger (ETH Zurich),
Wei Sun (Google),
Craig Gidney (Google),
Thomas Haner (ETH Zurich),
Hannah Sim (Harvard),
Vojtech Havlicek (Oxford),
Kanav Setia (Dartmouth),
Nicholas Rubin (Rigetti),
Matthew Neeley (Google) and
Dave Bacon (Google).

Questions?
----------

If you have any other questions, please contact help@openfermion.org.

Disclaimer
----------

Copyright 2017 The OpenFermion Developers.
This is not an official Google product.
