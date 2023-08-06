
=====
Django translation server
=====

Django translation server is a simple Django app to manage the project translations.

Obs: currently this projects only works with PostgreSQL database. Support for others databases will be added in future releases


Supported databases
-----------
- [x] PostgreSQL
- [ ] MySQL
- [ ] Sqlite



Requirements
-----------

Django REST framework - http://www.django-rest-framework.org/
django-filter
django-modeltranslation - http://django-modeltranslation.readthedocs.io/en/latest/installation.html#using-pip
PostgreSQL database - https://www.postgresql.org/
psycopg2 - https://pypi.python.org/pypi/psycopg2

Quick start
-----------

1. Add "translation_server" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'translation_server',
    ]

2. Include the Translation Server URLconf in your project urls.py like this::

    from django.conf.urls import url, include
    from rest_framework import routers
    from translation_server import views as translation_server_views

    router = routers.DefaultRouter()
    router.register(r'translation', translation_server_views.TranslationViewSet, 'translations')
    router.register(r'translation_type', translation_server_views.TranslationTypeViewSet, 'translations_types')

    urlpatterns = [
        ...
        url(r'^api/', include(router.urls, namespace='api'), ),
        url(r'^api/last_translation_tag/(?P<tag>\w+)[/]?$', translation_server_views.LastTranslationTagView.as_view(), name='get_last_translation_tag'),
        ...
    ]


3. Run ```python manage.py makemigraions``` and ```python manage.py migrate``` to create the Translation models, and load the initial data.

4. Run ```python manage.py collectstatic``` to collect the necessary static files.

5. Start the development server and visit http://127.0.0.1:8000/admin/ to create a translation (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/api/translation/ to view all translations

7. Run `python manage.py translate` to apply the basic translations for en-US and pt-BR
