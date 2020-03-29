# Global parameters
SHELL := /bin/bash
PYEXE := python3
PGK_NAME = randtest

# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "Commands for package management"
	@echo "make help"


## install:  Install package
.PHONY: install
install:
	$(PYEXE) -m pip install .


## develop:  Install development package
.PHONY: develop
develop:
	$(PYEXE) -m pip install -e .


## uninstall:  Uninstall (development) package
.PHONY: uninstall
uninstall:
	$(PYEXE) -m pip uninstall --yes $(PGK_NAME)


## dev-uninstall:  Uninstall (development) package
.PHONY: dev-uninstall
dev-uninstall:
	$(PYEXE) -m pip uninstall --yes $(PGK_NAME)
	rm -r $(PGK_NAME).egg-info


## example-smart-drug:  Run the smart drug example
.PHONY: example-smart-drug
example-smart-drug:
	$(PYEXE) examples/smart_drug.py


## tests:  Run tests
.PHONY: tests
tests:
	cd tests/; make tests; cd -


## rmdir:  Remove __pychache__ directories
.PHONY: rmdir
rmdir:
	find . -name __pycache__ -type d -exec rm -rf {} +
