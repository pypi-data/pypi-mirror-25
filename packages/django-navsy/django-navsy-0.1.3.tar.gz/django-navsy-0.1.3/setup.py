#!/usr/bin/env python

from setuptools import setup, find_packages

exec(open('navsy/version.py').read())

setup(
    name='django-navsy',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    version=__version__,
    description='django-navsy is a fast navigation system for lazy devs.',
    author='Fabio Caccamo',
    author_email='fabio.caccamo@gmail.com',
    url='https://github.com/fabiocaccamo/django-navsy',
    download_url='https://github.com/fabiocaccamo/django-navsy/archive/%s.tar.gz' % __version__,
    keywords=['django', 'navigation', 'nav', 'system', 'controller', 'router', 'routes', 'urls', 'pages', 'menu', 'breadcrumbs', 'tree', 'nodes', 'fast'],
    requires=['django(>=1.8)'],
    install_requires=[
        'django-autoslug >= 1.9.3, < 2.0.0',
        'python-slugify >= 1.2.4, < 1.3.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Build Tools',
    ],
    license='MIT',
    # test_suite='runtests.runtests'
)

