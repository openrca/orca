OpenRCA
==============================================

.. image:: https://img.shields.io/travis/openrca/orca.svg
   :target: https://travis-ci.org/openrca/orca

.. image:: https://img.shields.io/github/license/openrca/orca
   :target: https://github.com/openrca/orca

.. image:: https://img.shields.io/gitter/room/openrca/community
   :target: https://gitter.im/openrca/community

.. raw:: html

    <h2 align="center">
        <img src="docs/images/orca-logo.png" alt="OpenRCA" height="200px">
    <br>
    Automated Root Cause Analysis for Kubernetes
    </h2>

OpenRCA attempts to facilitate root cause inference of issues emerging in Kubernetes clusters. By
constructing a real-time cluster topology graph enriched with telemetry data obtained from
integrated telemetry sources (Prometheus, Elasticsearch, Falco, Istio, and others), provides
operators with a powerful analytical toolkit for dealing with daily application failures,
bottlenecks, and misconfigurations. Moreover, it comes with algorithms that leverage the collected
graph data to pinpoint sources of complex cluster defects.

Objectives
----------

- Holistic insight into application infrastructure (infra graph)
- Integration hub for telemetry projects (Prometheus, Elasticsearch, Falco and others)
- Time-based infrastructure analysis
- Automated diagnostics for common applications (databases, load balancers, message queues)
- ML-supported root cause inference
- Site reliability engineering and chaos testing

Installation
------------

Install using Helm chart:

::

    $ helm install ./helm/orca --namespace rca --name orca


Development
-----

Using Docker Compose:

::

    $ docker-compose build
    $ docker-compose up
    $ docker-compose down

Using Telepresence:

::

    $ telepresence \
        --namespace rca \
        --mount=/tmp/telepresence \
        --swap-deployment orca \
        --docker-run \
            --rm \
            -it \
            -v=/tmp/telepresence/var/run/secrets:/var/run/secrets \
            -v=/tmp/telepresence/etc/orca:/etc/orca \
            -v $(pwd):/app
