.PHONY: all deploy run freeze scheduler stylecheck

VENV=venv
BINUTILS=$(VENV)/bin

I18N_DIR=translations
DBPATH?=/tmp/rm

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -qr requirements.txt

freeze: $(VENV)
	@echo make sure that Jinja2 uses the patched 2.7.2 version: \
	@git+git://github.com/ikudriavtsev/jinja2.git@127e26e8ede5e0af3b4a3fe02f1690aa4a6484ff
	$(BINUTILS)/pip freeze >| requirements.txt

deploy: stylecheck
	git push

#run: deps
run:
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py remindme/*.py remindme/*/*.py

$(VENV):
	virtualenv $@

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


# init a new language
# e.g.: make translations/es
translations/%:
	locale=$$(echo $@ | cut -d/ -f2); \
	$(BINUTILS)/pybabel init -i messages.pot -d $@ -l $$locale; \
	curl "https://raw.githubusercontent.com/angular/angular.js/master/src/ngLocale/angular-locale_$$locale.js" \
		> static/js/angular-locale_$$locale.js
