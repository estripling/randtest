# Global parameters
SHELL := /bin/bash
PYEXE := python3

# Main
.PHONY: all help program
all: program

help: Makefile
	@sed -n 's/^##//p' $<

program:
	@echo "Commands for testing package"
	@echo "make help"


## tests:  Run tests
.PHONY: tests
tests:
	$(PYEXE) -m unittest test_randtest
