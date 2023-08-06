# pandascore-python

A [pandascore.co](https://pandascore.co) API client library for Python. Provides a simple interface that returns a dictionary of the JSON response. Supports Python 2.7 and 3.6

More information about the API is available at [PandaScore API Reference](https://api.pandascore.co/doc)

## Supported APIs

- Core API
- League of Legends API

## Getting Started

Install from PyPI:

```
pip install pandascore
```

Create an instance of PandaScore with your access token:

```
from pandascore import pandascore
ps = pandascore.PandaScore(access_token='put a token here')
```

Return a list of league dicts:

```
ps.get_leagues(videogame_id=1)
```

Or just get one league dict:

```
ps.get_league(league_id=2132)
```

## Testing

### Testing in virtualenv

Install into virtualenv:

```
make install-venv
source bin/activate
```

Run all tests:

```
make test
```

### Testing with Docker

Run the command below to build the docker container and run all tests:

```
make docker-test
```

### Testing multiple Python versions

We use tox to run test against multiple versions of Python. Tox requires the appropriate Python interpreters to run the tests in different environments. You can use pyenv for this. Once you've installed the appropriate interpreters, use this command to test in every environment:

```
make test-all
```
