.PHONY: test
test:
	@tox -e py37

.PHONY: lint
lint:
	@tox -e lint

.PHONY: docker-build
docker-build:
	@docker build . -f Dockerfile -t openrca/orca
