ORCA
==============================================

.. image:: https://img.shields.io/travis/openrca/orca.svg
    :target: https://travis-ci.org/openrca/orca

Installation
------------

TODO: Write installation instructions

Usage
-----

TODO: Write usage instructions

Development
-----

::

    $ telepresence \
        --namespace rca \
        --mount=/tmp/telepresence \
        --swap-deployment orca \
        --docker-run \
            --rm \
            -it \
            -v=/tmp/telepresence/var/run/secrets:/var/run/secrets \
            -v $(pwd):/app
