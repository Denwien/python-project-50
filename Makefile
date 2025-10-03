.PHONY: install run lint test clean

install:
	uv tool install --force .

run:
	python -m gendiff.scripts.gendiff -- -h

run-uv:
	uv run gendiff -- -f json file1.json file2.json

lint:
	ruff check .

test:
	pytest

clean:
	rm -rf build dist *.egg-info gendiff/__pycache__ gendiff/scripts/__pycache__
	find . -type f -name '*.pyc' -delete
