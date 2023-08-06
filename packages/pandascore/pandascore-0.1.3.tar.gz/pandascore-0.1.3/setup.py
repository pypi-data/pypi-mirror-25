import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'pandascore'
DESCRIPTION = 'A pandascore.co API client library for Python'
URL = 'https://github.com/tiamat-studios/pandascore-python'
EMAIL = 'adam.boscarino@tiamat-studios.com'
AUTHOR = 'Tiamat Studios'

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'PYPIREADME.rst')).read()
REQUIREMENTS = [
    line.strip()
    for line in open(
        os.path.join(here, 'requirements.txt'))
    .readlines()
]
TEST_REQUIREMENTS = [
    line.strip()
    for line in open(
        os.path.join(here, 'test-requirements.txt'))
    .readlines()
]

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=README,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests', )),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    test_requires=TEST_REQUIREMENTS,
    license='MIT License',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ], )
