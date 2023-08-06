# Endpointer

Endpointer is a cli tool to transform API specification documents into useful content for API documentation generation.

[![Build Status](https://travis-ci.org/devjack/endpointer.svg?branch=master)](https://travis-ci.org/devjack/endpointer)

## Usage

```
pip install endpointer
endpointer <your API spec.yml> combine | combined_spec.yml
```


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

_todo_

### Installing

If using a published version of endpointer:

```
pip install endpointer
```

For source installations:

```
pip install -e .
```

For development installs, build installs and other environments requiring
additional dependencies such as `pylint`, run:

```
pip install -e ".[dev]"
```


## Running the tests

Endpointer uses both doctest and unittest modules for test coverage. Both unit tests and doctests are run (together) by:

```
python setup.py test
```

And for linting (assumes pylint is available or you've installed .[dev] above)

```
pylint endpointer --disable=miscellaneous --ignore=cli
pylint endpointer/cli --disable=miscellaneous,duplicate-code
```

## examples

Definitions support JSON Schema pointers/$ref's:
```
>>> Definition({"a":{"b":{"$ref":"#/c/d"}},
...             "c":{"d":{"e":{"$ref":"#/h/i"}}},
...             "h":{"i":"hello"}}, "foo.yml"
... ).a.b.e
'hello'
```

## Deployment

To publish a new version of endpointer:
 * Bump the versions in `setup.py`
 * Ensure your local ~/.pypirc file is configured

First ensure:

```
pip install wheel twine
rm  -rf dist/*          # A clean dist directory
```

And then:

```
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
```


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and how to submit bugs. Pull requests would also be wonderful!

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/devjack/endpointer/tags).

## Authors

* **Jack Skinner** - *Founder* - [@developerjack](https://twitter.com/developerjack)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
