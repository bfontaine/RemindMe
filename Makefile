.PHONY: all deploy run scheduler stylecheck

VENV=venv
BINUTILS=$(VENV)/bin

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

deploy: stylecheck
	git push

run: deps
	CLOSURE_COMPRESSOR_OPTIMIZATION=ADVANCED_OPTIMIZATIONS \
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py pp/*.py

$(VENV):
	virtualenv $@
