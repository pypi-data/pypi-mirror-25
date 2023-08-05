.PHONY: clean coverage docker-test install-dev install-venv lint release test test-all

help:
	@echo "pandascore-python development. Use \`make <target>\`:"
	@echo "  clean          remove build products"
	@echo "  coverage       run coverage test"
	@echo "  docker-test    build docker container and run tests"
	@echo "  install-dev    install with test dependencies"
	@echo "  install-venv   install in virtualenv"
	@echo "  lint           run flake8"
	@echo "  release        build and upload"
	@echo "  test           run tests"
	@echo "  test-all       run tests on python 2.7 and 3.6"

clean:
	rm -rf *.egg *egg-info .cache .coverage .tox build bin include dist htmlcov lib
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf coverage.xml
	rm -rf pip-selfcheck.json

test: clean install-dev
	py.test tests

test-all: clean install-dev
	tox

lint:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 pandascore

coverage: clean install-dev
	pip install -q -e .[test]
	coverage run -m pytest tests
	coverage report --include='pandascore*'
	coverage html --include='pandascore*'

install-dev:
	pip install -r requirements.txt
	pip install -r test-requirements.txt
	pip install -e .

install-venv:
	virtualenv .
	bin/pip install -r requirements.txt
	bin/pip install -r test-requirements.txt
	bin/pip install -e .

docker-test: clean
	docker build -t "pypandascore-docker" .
	docker run pypandascore-docker

release:
	python setup.py sdist bdist_wheel
	twine upload dist/*
