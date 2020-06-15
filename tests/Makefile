# Global parameters
SHELL := /bin/bash
PYEXE = python3

# Function to run Python in virtual environment,
# needed for testing CLI functions.
define pyvenv
source ../venv/bin/activate; $(PYEXE) -m unittest ${1}; deactivate;
endef


# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "Commands for testing package"
	@echo "make help"


## tests ::  Run tests
.PHONY: tests
tests:
	$(call pyvenv, test_randtest)
