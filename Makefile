.PHONY: test
test:
	@tox

.PHONY: lint
lint:
	@tox -e lint

.PHONY: docker-build
docker-build:
	@docker build . -f Dockerfile -t openrca/orca
