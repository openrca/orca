.PHONY: format
format:
	@tox -e black

.PHONY: format-check
format-check:
	@tox -e black -- --check --diff .

.PHONY: lint
lint:
	@tox -e flake8

.PHONY: test
test:
	@tox -e py37

.PHONY: coverage
coverage:
	@tox -e coverage -- report --fail-under=90

.PHONY: docker-build
docker-build:
	@docker build . -f Dockerfile -t openrca/orca
