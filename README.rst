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

- Real-time cluster topology visualization
- Integration hub for telemetry data (Prometheus, Elasticsearch, Falco and others)
- Post-mortem analysis
- Automated root cause inference
- Diagnostics framework for common applications (databases, load balancers, message queues)
- Site reliability engineering and chaos testing

Installation
------------

Install using Helm chart:

::

    $ helm install ./helm/orca --namespace rca --name orca
