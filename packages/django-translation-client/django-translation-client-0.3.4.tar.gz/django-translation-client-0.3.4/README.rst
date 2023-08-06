
=====
Django translation client
=====

Django translation client is a simple Django app to sync the translations from the translation server to the project.


Requirements
-----------

requests
django-translation-server # Installed in local or remote server

Quick start
-----------

1. Add "translation_client" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'translation_client',
    ]

2. Add the "translation_server" URL like this::

    TRANSLATION_SERVER_URL = u"http://localhost:8000/api/translation"

3. Run `python manage.py sync_translation` to sync the server with the client.
