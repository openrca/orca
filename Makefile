.PHONY: test
test:
	@tox -e py37

.PHONY: lint
lint:
	@tox -e flake8

.PHONY: format
format:
	@tox -e black

.PHONY: format-check
format-check:
	@tox -e black -- --check --diff .

.PHONY: docker-build
docker-build:
	@docker build . -f Dockerfile -t openrca/orca
