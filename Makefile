
PACKAGE_NAME=trachet
DEPENDENCIES=tff
PYTHON=python
PYTHON26=python2.6
PYTHON27=python2.7
SETUP_SCRIPT=setup.py
RM=rm -rf
PIP=pip

.PHONY: smoketest nosetest build setuptools install uninstall clean update

all: build

setup_environment:
	if test -d tools; do \
		ln -f tools/gitignore .gitignore \
		ln -f tools/vimprojects .vimprojects \
    fi

build: update_license_block smoketest
	$(PYTHON) $(SETUP_SCRIPT) sdist
	$(PYTHON26) $(SETUP_SCRIPT) bdist_egg
	$(PYTHON27) $(SETUP_SCRIPT) bdist_egg

update_license_block:
	find . -type f -name '*.py' | \
		grep -v '^trachet/tff/' | \
		grep -v '^.git' | \
		xargs python tools/update_license.py

setuptools:
	$(PYTHON) -c "import setuptools" || \
		curl http://peak.telecommunity.com/dist/ez_$(SETUP_SCRIPT) | \
		$(PYTHON)

install: smoketest setuptools
	$(PYTHON) $(SETUP_SCRIPT) install

uninstall:
	for package in $(PACKAGE_NAME) $(DEPENDENCIES); \
	do \
		$(PIP) uninstall -y $$package; \
	done

clean:
	for name in dist build *.egg-info htmlcov cover *.egg; \
		do find . -type d -name $$name || true; \
	done | xargs $(RM)
	for name in *.pyc *.o; \
		do find . -type f -name $$name || true; \
	done | xargs $(RM)

test: smoketest nosetest

smoketest:
	$(PYTHON26) $(SETUP_SCRIPT) test
	$(PYTHON27) $(SETUP_SCRIPT) test

nosetest:
	if $$(which nosetests); \
	then \
	    nosetests --with-doctest \
	              --with-coverage \
	              --cover-html \
	              --cover-package=trachet; \
	fi

update: clean test
	$(PYTHON) $(SETUP_SCRIPT) register
	$(PYTHON) $(SETUP_SCRIPT) sdist upload
	$(PYTHON26) $(SETUP_SCRIPT) bdist_egg upload
	$(PYTHON27) $(SETUP_SCRIPT) bdist_egg upload

