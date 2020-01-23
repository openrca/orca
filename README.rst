OpenRCA
==============================================

.. image:: https://img.shields.io/travis/openrca/orca.svg
    :target: https://travis-ci.org/openrca/orca

.. image:: https://img.shields.io/github/license/openrca/orca
    :target: https://github.com/openrca/orca


---------------

Automated Root Cause Analysis for Kubernetes.

**Objectives:**

- Holistic insight into application infrastructure
- Time-based infrastructure analysis
- Automated diagnostic workflows (framework, workflow marketplace)
- ML-supported root cause inference
- Policy-driven RCA instrumentation
- Novel approach for site reliability testing and chaos engineering

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
