[![Build Status](https://travis-ci.org/fabiocaccamo/django-navsy.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-navsy)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-navsy/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-navsy)
[![Code Health](https://landscape.io/github/fabiocaccamo/django-navsy/master/landscape.svg?style=flat)](https://landscape.io/github/fabiocaccamo/django-navsy/master)
[![PyPI version](https://badge.fury.io/py/django-navsy.svg)](https://badge.fury.io/py/django-navsy)
[![Py versions](https://img.shields.io/pypi/pyversions/django-navsy.svg)](https://img.shields.io/pypi/pyversions/django-navsy.svg)
[![License](https://img.shields.io/pypi/l/django-navsy.svg)](https://img.shields.io/pypi/l/django-navsy.svg)

# django-navsy
django-navsy is a fast navigation system for lazy devs.

## Requirements
- Python 2.7, 3.4, 3.5, 3.6
- Django 1.8, 1.9, 1.10, 1.11

## Installation
1. Run ``pip install django-navsy`` or [download django-navsy](http://pypi.python.org/pypi/django-navsy) and add the **navsy** package to your project
2. Add ``'navsy'`` to ``settings.INSTALLED_APPS``
3. Add ``'navsy.context_processors.data'`` to context_processors:
```python
TEMPLATES = [
    {
        # ...
        'OPTIONS': {
            'context_processors': [
                # ...
                'navsy.context_processors.data',
                # ...
            ],
        },
        # ...
    },
]
```
4. Add ``'navsy.urls'`` to ``urls.py``
```python
# single-language application
from django.conf.urls import include, url

# ...
urlpatterns += [url(r'^', include('navsy.urls'))]
```
```python
# multi-language application
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

# ...
urlpatterns += [url(r'^i18n/', include('django.conf.urls.i18n'))]
urlpatterns += i18n_patterns(url(r'^', include('navsy.urls')))
```

5. Run ``python manage.py migrate navsy``
6. Run ``python manage.py collectstatic``
7. Restart your application server
8. Open the admin and enjoy :)

## License
Released under [MIT License](LICENSE).
