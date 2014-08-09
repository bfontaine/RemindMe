.PHONY: all deploy run freeze scheduler stylecheck bootstrap

VENV=./venv
BINUTILS=$(VENV)/bin

DBPATH?=/tmp/rm

I18N_DIR=translations
LOCALES=en fr

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

freeze: $(VENV)
	@echo make sure that Jinja2 uses the patched 2.7.2 version: \
	@git+git://github.com/ikudriavtsev/jinja2.git@127e26e8ede5e0af3b4a3fe02f1690aa4a6484ff
	$(BINUTILS)/pip freeze >| requirements.txt

deploy: stylecheck
	git push

run:
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py remindme/*.py remindme/*/*.py

$(VENV):
	virtualenv $@

bootstrap: deps babel-compile

# DB

startdb:
	mkdir -p $(DBPATH)
	mongod --dbpath=$(DBPATH)

# I18N

babel-extract:
	$(BINUTILS)/pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	$(BINUTILS)/pybabel update -i messages.pot -d $(I18N_DIR)

babel-compile:
	$(BINUTILS)/pybabel compile -d $(I18N_DIR)
