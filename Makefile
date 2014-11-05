.PHONY: all deploy run freeze scheduler stylecheck bootstrap check covercheck \
	compile-assets

SRC=remindme

VENV=./venv
BINUTILS=$(VENV)/bin

DBPATH?=/tmp/rm

I18N_DIR=translations

PIP=$(BINUTILS)/pip
PYBABEL=$(BINUTILS)/pybabel

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

PROD_REMOTE=prod
PROD_BRANCH=master

all: run

deps: $(VENV)
	$(BINUTILS)/pip install -r requirements.txt

freeze: $(VENV)
	@echo make sure that Jinja2 uses the patched 2.7.2 version: \
	 git+https://github.com/ikudriavtsev/jinja2.git@127e26e8ede5e0af3b4a3fe02f1690aa4a6484ff
	$(PIP) freeze >| requirements.txt

deploy: stylecheck
	git push $(PROD_REMOTE) $(PROD_BRANCH)

run:
	$(BINUTILS)/gunicorn app:app

scheduler: deps
	$(BINUTILS)/python scheduler.py

stylecheck: *.py deps
	$(BINUTILS)/pep8 *.py remindme/*.py remindme/*/*.py

$(VENV):
	virtualenv $@

bootstrap: deps babel-compile

# Assets

compile-assets: static/css/app.css

static/css/app.css: static/css/*.less
	lessc static/css/app.less > $@

# DB

startdb:
	mkdir -p $(DBPATH)
	mongod --dbpath=$(DBPATH)

# I18N

babel-extract:
	$(PYBABEL) extract -F babel.cfg -k lazy_gettext -o messages.pot .
	$(PYBABEL) update -i messages.pot -d $(I18N_DIR)

babel-compile:
	$(PYBABEL) compile -d $(I18N_DIR)

# Tests

check:
	$(BINUTILS)/python tests/test.py

covercheck:
	$(BINUTILS)/coverage run --source=$(SRC) tests/test.py
	$(BINUTILS)/coverage $(COVERAGE_REPORT)

coverhtml:
	@make COVERAGE_REPORT=html covercheck
	@echo '--> open htmlcov/index.html'
