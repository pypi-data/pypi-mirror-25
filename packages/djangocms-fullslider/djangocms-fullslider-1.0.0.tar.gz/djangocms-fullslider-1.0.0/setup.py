"""
Full page slider plugin for django CMS
See: https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

version = "1.0.0"
root_dir = path.abspath(path.dirname(__file__))

with open(path.join(root_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='djangocms-fullslider',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='Full page slider plugin for django CMS',
    long_description=long_description,
    keywords='django cms plugin fullpage slider background image',

    # The project's main homepage.
    url='https://github.com/Logicify/djangocms-fullslider',

    # Author details
    author='Dmitriy Selischev',
    author_email='dmitriy.selischev@logicify.com',

    # License
    license='MIT',

    # Technical meta
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Who this project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # License (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Python versions support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Structure
    packages=find_packages(exclude=['contrib', 'docs', 'tests'], include=['djangocms_fullslider']),

    # Dependencies
    install_requires=[
        'django',
        'django-cms',
        'django-sekizai',
        'cmsplugin-filer',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': [],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },
)
