# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.1'


setup(
    name='django-shell',
    version=version,
    keywords='django-shell',
    description='Django Shell Functions',
    long_description=open('README.rst').read(),

    url='https://github.com/django-xxx/django-shell',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['djshell'],
    py_modules=[],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)
