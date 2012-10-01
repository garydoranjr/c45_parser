A C4.5 Parser
=============

by Gary Doran (<gdb6@case.edu>) and Tim Henderson (<tim.tadh@gmail.com>).

For parsering datasets in the
[C4.5 dataformat](http://www.cs.washington.edu/dm/vfml/appendixes/c45.htm)

Installation
------------

This package can be installed in two ways (the easy way):

    pip install -e git+https://github.com/garydoranjr/mldata.git#egg=c45_parser

or by running the setup file manually

    git clone [the url for c45_parser]
    cd c45_parser
    python setup.py install

Note the code depends on the `numpy` and `scipy` packages. So have those
installed first. The build will likely fail if it can't find them.

How To Use
==========

After installation, you can simply import the c45\_parser and use it.

    from c45_parser import load_c45
    examples = load_c45(dataset, inputdir)

The most useful function will likely be `load_c45`, which locates the
appropriate '.names' and '.data' files within some subdirectory of the current
working directory, and parses them to return an `ExampleSet`. The load\_c45
function takes to arguments: 1) the name of the dataset, 2) the input directory.
See the docstrings for details on these functions and classes.

The implementation of the parser is in `c45_parser/mldata.py`. This file
contains the code for parsing C4.5 format files, and representing the data with
some type safety.  The other files include some example data, and a unit test.
This code has been tested with Python 2.6 and Python 2.7.

c45\_to\_matlab script
----------------------

There is a script included to convert c4.5 datasets to datasets appropriate for
matlab. To use it (in the c45\_parser directory containing: example.data,
example.names):

    c45_to_matlab -d . -o example.mat examples

which creates the example.mat file.

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
Doran at <gbd6@case.edu> (you can also contact Tim Henderson at
<tim.tadh@gmail.com>).

