from setuptools import setup

AUTHOR = 'hirschbeutel'
AUTHOR_EMAIL = 'hirschbeutel@gmail.com'
DESCRIPTION = 'Bruker Opus FTIR spectroscopy clone'
NAME = 'ono'
URL='https://hirschbeutel@bitbucket.org/hirschbeutel/ono'

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
VERSION = '0.1.2'

setup(
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license='LGPL',
        name=NAME,
        packages=[NAME],
        url=URL,
        version=VERSION)
