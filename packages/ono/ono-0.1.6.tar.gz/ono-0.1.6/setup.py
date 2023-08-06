from setuptools import setup

AUTHOR = 'hirschbeutel'
AUTHOR_EMAIL = 'hirschbeutel@gmail.com'
DESCRIPTION = 'Bruker Opus FTIR spectroscopy clone'
LONG_DESCRIPTION = 'Bruker Opus FTIR spectroscopy clone'
NAME = 'ono'
URL='https://hirschbeutel@bitbucket.org/hirschbeutel/ono'

with open('VERSION') as version_file:
    VERSION = version_file.read().strip()

setup(
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license='LGPL',
        long_description=LONG_DESCRIPTION,
        name=NAME,
        packages=[NAME],
        # setup_requires=['setuptools_scm'],
        # use_scm_version=True,
        version=VERSION,
        url=URL,)
