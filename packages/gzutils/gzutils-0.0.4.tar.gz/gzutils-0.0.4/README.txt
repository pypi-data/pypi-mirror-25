Gizur Misc Utils
=================

This package contains the following classes/functions:

* A `Logging class` - simple base class for logging
* The `DotDict`  class- make it possible to access dictionary attributes with dot-notation
(`dict.attribute` instead of `dict['attribute']`)
* Functions for saving CSV files from lists


Development
----------

Build the package for distribution with: `python setup.py sdist`

Publish a build with: `twine upload dist/gzutils-X.Y.Z.tar.gz`
