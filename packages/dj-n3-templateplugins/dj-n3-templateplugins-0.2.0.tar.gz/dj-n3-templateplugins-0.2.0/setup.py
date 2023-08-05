#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys


asdf = '0.2.0'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from dj_n3_templateplugins/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("dj_n3_templateplugins", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dj-n3-templateplugins',
    version=version,
    description="""Extensible Template Plugins for Django""",
    long_description=readme + '\n\n' + history,
    author='Jared Newell',
    author_email='jared.newell@gmail.com',
    url='https://github.com/Jaredn/dj-n3-templateplugins',
    download_url='https://github.com/Jaredn/dj-n3-templateplugins/archive/0.2.0.tar.giz',
    packages=[
        'dj_n3_templateplugins',
    ],
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords='dj-n3-templateplugins django plugins template templateplugin',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
