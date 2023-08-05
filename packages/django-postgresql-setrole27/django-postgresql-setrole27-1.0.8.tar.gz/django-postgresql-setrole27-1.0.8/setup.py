#!/usr/bin/env python
# -* encoding: utf-8 *-
from __future__ import absolute_import
import os
from setuptools import setup
from io import open

HERE = os.path.dirname(__file__)

try:
    long_description = open(os.path.join(HERE, u'README.rst')).read()
except IOError:
    long_description = None


setup(
    name=u"django-postgresql-setrole27",
    version=u"1.0.8",
    packages=[u"postgresql_setrole27"],
    classifiers=[
        u"Development Status :: 5 - Production/Stable",
        u"Intended Audience :: Developers",
        u"Intended Audience :: System Administrators",
        u"Programming Language :: Python :: 3 :: Only",
        u"License :: OSI Approved :: BSD License",
        u"Operating System :: POSIX",
    ],
    url=u"https://github.com/jdelic/django-postgresql-setrole/",
    author=u"Jonas Maurus (@jdelic)",
    author_email=u"jonas-postgresql-setrole@gopythongo.com",
    maintainer=u"GoPythonGo.com",
    maintainer_email=u"info@gopythongo.com",
    description=u"Execute SET ROLE on every PostgreSQL connection in the Django ORM",
    long_description=long_description,
)
