#!/usr/bin/env python
#
# NOTE: when testing, use "pip install ... --upgrade"

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2011-2013, University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

# Setup.py based on https://github.com/paltman/python-setup-template/blob/master/setup.py,
# following http://www.ibm.com/developerworks/opensource/library/os-pythonpackaging/index.html
#
# These could be useful:
#   https://wiki.python.org/moin/Distutils/Tutorial
#   https://pypi.python.org/pypi/check-manifest


import codecs
import os
import sys

from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages
from pip.req import parse_requirements      # See: http://stackoverflow.com/questions/14399534/

dir_here = os.path.dirname(__file__)
# sys.path.insert(0, os.path.join(dir_here, "annalist_site"))

# Helper to load README.md, etc.
def read(fname):
    return codecs.open(os.path.join(dir_here, fname)).read()

PACKAGE         = "annalist_root.annalist"
PACKAGE_MODULE  = __import__(PACKAGE, globals(), locals(), ['__version__', '__author__'])
VERSION         = PACKAGE_MODULE.__version__
AUTHOR          = PACKAGE_MODULE.__author__
AUTHOR_EMAIL    = "gk-pypi@ninebynine.org"
NAME            = "Annalist"
DESCRIPTION     = "Annalist linked data notebook"
URL             = "https://github.com/gklyne/annalist"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages = 
        [ 'annalist_root'
          , 'annalist_root.annalist'
            , 'annalist_root.annalist.models'
            , 'annalist_root.annalist.views'
            , 'annalist_root.annalist.views.fields'
            , 'annalist_root.annalist.tests'
          , 'annalist_root.annalist_site'
            , 'annalist_root.annalist_site.settings'
          , 'annalist_root.utils'
          , 'annalist_root.oauth2'
          , 'annalist_root.miscutils'
            , 'annalist_root.miscutils.test'
        ],
    package_dir = 
        { 'annalist_root':  'annalist_root'
        # , 'annalist':       'annalist_root/annalist'
        # , 'annalist_site':  'annalist_root/annalist_site'
        # , 'utils':          'annalist_root/annalist'
        # , 'oauth2':         'annalist_root/utils'
        # , 'miscutils':      'annalist_root/miscutils'
        },
    package_data = 
        { 'annalist_root':
            [ '*.sh', '*.txt'
            , 'sampledata/README.md'
            , 'sampledata/init/annalist_site/README.md'
            , 'sampledata/init/annalist_site/_annalist_site/*.jsonld'
            , 'sampledata/init/annalist_site/c/*/_annalist_collection/*.jsonld'
            , 'sampledata/init/annalist_site/c/*/_annalist_collection/lists/*/*.jsonld'
            , 'sampledata/init/annalist_site/c/*/_annalist_collection/types/*/*.jsonld'
            , 'sampledata/init/annalist_site/c/*/_annalist_collection/views/*/*.jsonld'
            , 'sampledata/init/annalist_site/c/*/d/*/*/*.jsonld'
            , 'sampledata/data/annalist_site/README.md'
            # , 'sampledata/data/annalist_site/_annalist_site/*.jsonld'
            ]
        , 'annalist_root.annalist':
            [ 'templates/*.html'
            , 'templates/field/*.html'
            , 'static/css/*.css'
            , 'static/js/*.css'
            , 'static/images/*.png'
            , 'static/images/icons/warning_32.png'
            , 'static/images/icons/search_32.png'
            , 'static/foundation/css/*.css'
            # , 'static/foundation/img/*.png'
            , 'static/foundation/js/foundation/*.js'
            , 'static/foundation/js/vendor/*.js'
            , 'sitedata/enums/*/*/*.jsonld'
            , 'sitedata/fields/*/*.jsonld'
            , 'sitedata/lists/*/*.jsonld'
            , 'sitedata/types/*/*.jsonld'
            , 'sitedata/views/*/*.jsonld'
            ],
        },
    exclude_package_data = {
        '': ['spike/*'] 
        },
    data_files = 
        [
        ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers, Researchers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    zip_safe=False,
    install_requires=
        [ 'Django==1.7'
          , 'wsgiref==0.1.2'
        , 'oauth2client==1.2'
          , 'httplib2==0.9'
        , 'pyparsing==2.0.2'    # Does RDFlib need 1.5.7?
        # For testing:
        , 'beautifulsoup4'
        # For development - used by miscutils/MockHttpResources:
        # , 'httpretty==0.7.1'
        # Probably used by RDFlib stuff..
        # , 'SPARQLWrapper==1.5.2'
        # , 'html5lib==1.0b3'
        # , 'isodate==0.4.9'
        # , 'six==1.4.1'
        ]

    # entry_points = {
    #     'console_scripts': [
    #         ],
    #     },
    )


# (Leftover from previous setup?)
# standard_exclude = ["*.py", "*.pyc", "*$py.class", "*~", ".*", "*.bak"]
# standard_exclude_directories = [
#     ".*", "CVS", "_darcs", "./build", "./dist", "EGG-INFO", "*.egg-info"
# ]


# # parse_requirements() returns generator of pip.req.InstallRequirement objects
# # reqs is a list of requirement; e.g. ['django==1.5.1', 'mezzanine==1.4.6']
# install_reqs = parse_requirements(os.path.join(dir_here, "requirements/devel.txt"))
# reqs         = [str(ir.req) for ir in install_reqs]

