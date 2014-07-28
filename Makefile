.PHONY: all deploy run freeze scheduler stylecheck

VENV=venv
BINUTILS=$(VENV)/bin

I18N_DIR=translations
DBPATH?=/tmp/rm

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

freeze: $(VENV)
	$(BINUTILS)/pip freeze >| requirements.txt

deploy: stylecheck
	git push

run: deps
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py remindme/*.py remindme/*/*.py

$(VENV):
	virtualenv $@

# DB

startdb:
	mongod --dbpath=$(DBPATH)

# I18N

babel-extract:
	$(BINUTILS)/pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	$(BINUTILS)/pybabel update -i messages.pot -d $(I18N_DIR)

babel-compile:
	$(BINUTILS)/pybabel compile -d $(I18N_DIR)
