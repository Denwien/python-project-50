.PHONY: lint test test-coverage check

lint:
	flake8 gendiff

test:
	pytest tests/

test-coverage:
	pytest --cov=gendiff tests/

check: lint test-coverage
