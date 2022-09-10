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
	@docker build . -f Dockerfile -t openrca/orca
