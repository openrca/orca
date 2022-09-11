IMAGE ?= openrca/orca

.PHONY: format
format:
	@tox -e test-tools -- black .

.PHONY: format-check
format-check:
	@tox -e test-tools -- black --check --diff .

.PHONY: lint
lint:
	@tox -e test-tools -- flake8 .

.PHONY: test
test:
	@tox -e py37

.PHONY: coverage
coverage:
	@tox -e test-tools -- coverage report --fail-under=90

.PHONY: docker-build
docker-build:
	@docker build . -f Dockerfile -t $(IMAGE)

.PHONY: docker-scan
docker-scan:
	@docker scan --accept-license --file Dockerfile --dependency-tree $(IMAGE)
