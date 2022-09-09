PY = py37
s
.PHONY: test
test:
	tox -e $(PY) $(OPTIONS)

.PHONY: lint
lint:
	tox -e lint
