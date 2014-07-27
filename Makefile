.PHONY: all deploy run freeze scheduler stylecheck

VENV=venv
BINUTILS=$(VENV)/bin
I18N_DIR=translations

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

freeze: $(VENV)
	$(BINUTILS)/pip freeze >| requirements.txt

deploy: stylecheck
	git push

run: deps
	CLOSURE_COMPRESSOR_OPTIMIZATION=ADVANCED_OPTIMIZATIONS \
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py remindme/*.py remindme/*/*.py

$(VENV):
	virtualenv $@

babel-extract:
	$(BINUTILS)/pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .

babel-compile:
	$(BINUTILS)/pybabel compile -d $(I18N_DIR)
