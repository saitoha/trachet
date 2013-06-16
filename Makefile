
PACKAGE_NAME=trachet
PYTHON=python

.PHONY: test

all: test
	$(PYTHON) setup.py sdist
	python2.6 setup.py bdist_egg
	python2.7 setup.py bdist_egg

install: test 
	$(PYTHON) -c "import setuptools" || curl http://peak.telecommunity.com/dist/ez_setup.py | python
	$(PYTHON) setup.py install

uninstall:
	yes | pip uninstall $(PACKAGE_NAME) 
	
clean:
	rm -rf dist/ build/ *.egg-info *.pyc **/*.pyc

test:
	$(PYTHON) setup.py test

update: clean test
	$(PYTHON) setup.py register
	$(PYTHON) setup.py sdist upload
	python2.6 setup.py bdist_egg upload
	python2.7 setup.py bdist_egg upload

