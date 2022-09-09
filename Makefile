PY = py37

.PHONY: test
test:
	@tox -e $(PY) $(OPTIONS)

.PHONY: lint
lint:
	@tox -e lint
