# Contributing to OpenRCA

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to OpenRCA and its packages, which are hosted in the [OpenRCA Organization](https://github.com/openrca) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[How can I contribute?](#how-can-i-contribute)

[Development environment](#development-environment)
  * [Setting up Python](#setting-up-python)
  * [Setting up Docker](#setting-up-docker)
  * [Setting up Kubernetes](#setting-up-kubernetes)
  * [Setting up Telepresence](#setting-up-telepresence)
  * [Installing OpenRCA](#installing-openrca)
  * [Using Telepresence](#using-telepresence)

[Workflow](#workflow)
  * [Pull requests](#pull-requests)
  * [Issues](#pull-requests)

[Styleguides](#styleguides)
  * [Git commit messages](#git-commit-messages)


## How can I contribute?

**Feeling ready to contribute? Great! For sure, you will find exciting features to carve!**

First, please review the reported bugs and feature requests in
[Github issues](https://github.com/openrca/orca/issues). As a new contributor, give priority to
items labeled "*good first issue*". These tasks have a reasonable level of complexity intended for
newcomers, and at the same time, enable you to familiarize yourself with a significant part of the
codebase. They also allow going through the Github workflow and CI process for the first time.

If nothing caught your eye or you need a more individual approach, don't hesitate to contact us in
our Gitter chat. We will introduce you to the project and openly talk about other options in the
roadmap.

## Development environment

To help you get started, below is a curated list of steps needed to prepare a development
environment. We didn't bother writing detailed instructions for each tool, because others did it
well a long time ago. Most steps will redirect you to trusted sources with complete setup
instructions.

### Setting up Python

Many OpenRCA components are written in the Python programming language. To build, you'll need a
Python development environment. If you haven't already, please follow
[these](https://docs.python.org/3/using/index.html) instructions to install Python with the required
toolset.

OpenRCA currently builds with Python 3.7.

### Setting up Docker

OpenRCA has a Docker build system for creating and publishing Docker images. To leverage that, you
will need a Docker engine installed in your system. To download and install Docker follow
[these instructions](https://docs.docker.com/install/).

### Setting up Kubernetes

OpenRCA requires Kubernetes version 1.14 or higher. Follow the steps outlined
[here](https://kubernetes.io/docs/setup/) to choose installation option appropriate for your
conditions.

Note, some OpenRCA functionality may not work with latest Kubernetes releases. Analyze the
[compatibility matrix](https://github.com/kubernetes-client/python#compatibility-matrix) for
the Kubernetes Python client library to check if the release of your choice is supported. The
library is often a few releases behind Kubernetes master.

### Setting up Telepresence

[Telepresence](https://www.telepresence.io) is an optional tool that most OpenRCA developers choose
for integrating new features. It enables running your code seamlessly in a Kubernetes cluster.
Follow [these](https://www.telepresence.io/reference/install) instructions to setup Telepresence in
your system.

### Installing OpenRCA

Install OpenRCA in your Kubernetes cluster by following steps in the
[documentation](https://openrca.io/docs/).

### Using Telepresence

When ready to test an implemented feature, use the following Telepresence command to evaluate it in
a Kubernetes cluster:

```
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
```

The command above swaps the deployment specified by `--namespace` and `--swap-deployment` flags with
a Docker container started in your local station using parameters provided via `--docker-run` flag.
Besides, it attaches secrets and config maps from the Kubernetes cluster to the local container.

## Workflow

### Pull requests

If you're working on an existing issue, respond to the issue and express interest in working on it.
This helps other people know that the issue is active, and hopefully prevents duplicated efforts.

To submit a proposed change:

- [Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) the affected
  repository.
- Create a new branch for your changes.
- Develop the code/fix.
- Add new test scenarios. In the case of a bug fix, the tests should fail without your code changes.
  For new features try to cover as many variants as reasonably possible.
- Modify the documentation as necessary.
- Verify the entire CI process (building and testing) works.

While there may be exceptions, the general rule is that all PRs should be 100% complete - meaning
they should include all test cases and documentation changes related to the change.

### Issues

[GitHub issues](https://github.com/openrca/orca/issues/new) can be used to report bugs or
submit feature requests.

When reporting a bug please include the following key pieces of information:

- The version of the project you were using (e.g. version number, or git commit).
- The exact, minimal, steps needed to reproduce the issue. Submitting a 5 line script will get
  a much faster response from the team than one that's hundreds of lines long.

## Styleguides

### Git commit messages

* Use the present tense ("Add probe for..." not "Added probe for...").
* Use the imperative mood ("Add probe for..." not "Adds probe for...").
* Limit the first line to 72 characters or less.
* Reference issues and pull requests liberally after the first line.
