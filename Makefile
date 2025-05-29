.PHONY: all lint test test-cov install dev clean distclean

PYTHON ?= python

all: ;

lint:
	-q2lint || echo "q2lint failed but continuing..."
	flake8

test: all
	py.test

test-cov: all
	py.test --cov=q2_SCNIC

install: all
	$(PYTHON) setup.py install

dev: all
	pip install -e .

clean: distclean

distclean: ;