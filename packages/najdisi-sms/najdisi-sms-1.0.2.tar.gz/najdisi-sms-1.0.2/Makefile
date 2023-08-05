.PHONY: all test install clean

all:
	@echo "Commands:"
	@echo "    make install - Install to system"
	@echo "    make test - Run test"
	@echo "    make venv - Create a virtual environment"
	@echo "    make clean - Clean venv and git ignore files"

install:
	@type pip || { echo "ERROR: Please install python-pip!"; exit 1; }
	pip install .

test: venv
	venv/bin/python setup.py test

venv:
	virtualenv --no-site-packages venv
	venv/bin/pip install -e .[tests,docs]

clean :
	git clean -f -X -d
