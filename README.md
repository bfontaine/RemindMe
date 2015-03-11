# RemindMe

## Set Up

    make bootstrap

You need to install LESS:

    [sudo] npm -g install less

## Run

You have to run three different jobs:

  # run the DB
  make startdb

  # run the app
  make run

  # run the scheduler
  make scheduler


## i18n

### Adding a locale

As an example, let’s say we want to add the spanish locale: `es`. We need to
initialize the l10n files:

    venv/bin/pybabel init -i messages.pot -d translations -l es
    curl "https://raw.githubusercontent.com/angular/angular.js/master/src/ngLocale/angular-locale_es.js" > static/js/angular-locale_es.js
    make babel-extract

Now edit `translations/es/LC_MESSAGES/messages.po`, then compile it:

    make babel-compile

That’s it.
