How To Use
==========

All the code you will need to use is in `mldata.py`. This file contains the code
for parsing C4.5 format files, and representing the data with some type safety.
The other files include some example data, and a unit test.  This code has been
tested with Python 2.6 and Python 2.7.

Simply place the `mldata.py` module into your source directory, and use
`from mldata import *` within your other modules to import the
relevant functions and classes. The most useful function will likely be
`parse_c45`, which locates the appropriate '.names' and '.data' files
within some subdirectory of the current working directory, and parses them to
return an `ExampleSet`. See the docstrings for details on these
functions and classes.

Hints
=====

An `Example` is a list of `Feature`s that complies with some `Schema`, which
describes feature types and values. An `ExampleSet` is a list of `Example`s that
all comply with the same `Schema`.

`ExampleSet`s, `Example`s, and `Schema`s all implement the necessary sequence
methods so that syntax like:

    >>> dataset[i][j]

gives the value of the `j`th feature of the `i`th example, and:

    >>> for example in dataset: ...

iterates through examples in the dataset. To select a particular subset of an
example set, you can use Python's useful list comprehension/generator syntax as
in:

    >>> subset = ExampleSet(ex for ex in dataset if ex[2] == 'Monday')

Note that an example's class label is always the last feature, so
`example[-1]` is the label of an example, and
`example[:-1]` is a list of 'proper' features.

For assignments that require a matrix representation of data, you may want to
consider using [NumPy](http://numpy.scipy.org/). Using the `to_float` method of
the `ExampleSet`, you can easily convert to NumPy arrays as in:

    >>> data_array = numpy.array(dataset.to_float())

Questions and Issues
====================

If you find any bugs or have any questions about this code, please create an
issue on [GitHub](https://github.com/garydoranjr/mldata/issues), or contact Gary
Doran at <gbd6@case.edu>.
