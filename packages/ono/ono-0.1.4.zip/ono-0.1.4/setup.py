from setuptools import setup

AUTHOR = 'hirschbeutel'
AUTHOR_EMAIL = 'hirschbeutel@gmail.com'
DESCRIPTION = 'Bruker Opus FTIR spectroscopy clone'
NAME = 'ono'
URL='https://hirschbeutel@bitbucket.org/hirschbeutel/ono'

# VERSION should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
# VERSION = '0.1.2'

with open('VERSION') as version_file:
    VERSION = version_file.read().strip()

setup(
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license='LGPL',
        name=NAME,
        packages=[NAME],
        # setup_requires=['setuptools_scm'],
        # use_scm_version=True,
        version=VERSION,
        url=URL,)
