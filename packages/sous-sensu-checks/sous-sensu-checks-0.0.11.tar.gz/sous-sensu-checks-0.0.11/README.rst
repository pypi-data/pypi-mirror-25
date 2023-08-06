sous-sensu-checks
==================
Calls otpl-service-check for each compatible deployment found in a sous
global deploy manifest (GDM).

Writes the results of these checks to the local Sensu client.

Usage
-----
This script is long running, and performs periodic checks,
delivering the results directly to Sensu on ``localhost:3030``.

Dependencies
------------
See ``requirements.txt``.

Notably, see https://github.com/opentable/otpl-service-check
which this script wraps.

Arguments
---------
Run with ``-h`` or ``--help`` to see command-line argument
documentation.

Releasing
---------

Set up PyPI RC file, .pypirc. E.g.:

    [distutils]
    index-servers =
      pypi
      pypitest

    [pypitest]
    repository = https://testpypi.python.org/pypi
    username = cpennello_opentable

    [pypi]
    repository = https://pypi.python.org/pypi
    username = cpennello_opentable

Suppose the version being released is a.b.c.

Create distributions:

``python setup.py sdist bdist_wheel``

Sign distribution files:

    for x in dist/*a.b.c*;do
      gpg --detach-sign -a $x
    done

Use Twine, uploading to the test repo first.

``twine upload -r pypitest dist/*a.b.c*``

Then to the real repo.

``twine upload -r pypi dist/*a.b.c*``
