# RemindMe

## Set Up

    make bootstrap

## i18n

### Adding a locale

As an example, let’s say we want to add the spanish locale: `es`. We need to
initialize the l10n files:

    venv/bin/pybabel init -i messages.pot -d translations/es -l es
    curl "https://raw.githubusercontent.com/angular/angular.js/master/src/ngLocale/angular-locale_es.js" > static/js/angular-locale_es.js
    make babel-extract

Now edit `translations/es/LC_MESSAGES/messages.mo`, then compile it:

    make babel-compile

That’s it.
