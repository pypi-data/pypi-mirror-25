#!/usr/bin/env python
import io

from setuptools import setup, find_packages


def _read(filename, as_lines=True):
    with io.open(filename, encoding='utf-8') as handle:
        if as_lines:
            return [line.strip('\n').strip() for line in handle.readlines()]
        return handle.read()


setup(
    name='wagtailnest',
    version='0.0.6',
    description='A RESTful Wagtail enclosure',
    long_description=_read('README.md', as_lines=False),
    author='Ionata Digital',
    author_email='webmaster@ionata.com.au',
    url='https://github.com/ionata/wagtailnest',
    packages=find_packages('src'),
    install_requires=_read('requirements-production.txt'),
    extras_require={
        'defaults': _read('requirements-defaults.txt'),
    },
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
