# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = __import__('fairepart').__version__

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, 'README.rst')) as f:
    README = f.read()

setup(
    name='django-fairepart',
    version=version,
    description='A generic application to invite your contact from facebook, google, etc.',
    long_description=README,
    author='Florent Messa',
    author_email='florent.messa@gmail.com',
    url='http://github.com/thoas/django-fairepart',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'facepy',
        'python-social-auth',
        'gdata',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ]
)
