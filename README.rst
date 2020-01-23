OpenRCA
==============================================

.. image:: https://img.shields.io/travis/openrca/orca.svg
    :target: https://travis-ci.org/openrca/orca

Automated Root Cause Analysis for Kubernetes.

Installation
------------

Install using Helm chart:

::

    $ helm install ./orca --namespace rca --name orca

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
