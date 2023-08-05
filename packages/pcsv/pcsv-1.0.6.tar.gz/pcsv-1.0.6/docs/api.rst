.. api.rst
.. Copyright (c) 2013-2017 Pablo Acosta-Serafini
.. See LICENSE for details

.. _NonNegativeInteger:
   http://pexdoc.readthedocs.io/en/stable/ptypes.html#nonnegativeinteger
.. _FileName:
   http://pexdoc.readthedocs.io/en/stable/ptypes.html#filename
.. _FileNameExists:
   http://pexdoc.readthedocs.io/en/stable/ptypes.html#filenameexists

###
API
###

*******************************
Identifying (filtering) columns
*******************************

Several class methods and functions in this module allow column and row
filtering of the CSV file data. It is necessary to identify columns for both
of these operations and how these columns can be identified depends on whether
the file has or does not have a header as indicated by the **has_header**
boolean constructor argument:

* If **has_header** is :code:`True` the first line of the file is taken as the
  header.  Columns can be identified by name (a string that has to match a
  column value in the file header) or by number (an integer representing the
  column number with column zero being the leftmost column)

* If **has_header** is :code:`False` columns can only be identified by number
  (an integer representing the column number with column zero being the
  leftmost column)

For example, if a file ``myfile.csv`` has the following data:

+------+-----+--------+
| Ctrl | Ref | Result |
+======+=====+========+
|    1 |   3 |     10 |
+------+-----+--------+
|    1 |   4 |     20 |
+------+-----+--------+
|    2 |   4 |     30 |
+------+-----+--------+
|    2 |   5 |     40 |
+------+-----+--------+
|    3 |   5 |     50 |
+------+-----+--------+

Then when the file is loaded with
:code:`pcsv.CsvFile('myfile.csv', has_header=True)` the columns can be
referred to as :code:`'Ctrl'` or :code:`0`, :code:`'Ref'` or :code:`1`, or
:code:`'Result'` or :code:`2`. However if the file is loaded with
:code:`pcsv.CsvFile('myfile.csv', has_header=False)` the columns can
be referred only as :code:`0`, :code:`1` or :code:`2`.

**************
Filtering rows
**************

Several class methods and functions of this module allow row filtering of the
CSV file data. The row filter is described in the :ref:`CsvRowFilter`
pseudo-type

*****************************
Swapping or inserting columns
*****************************

The column filter not only filters columns *but also* determines the order in
which the columns are stored internally in an :py:class:`pcsv.CsvFile`
object. This means that the column filter can be used to reorder and/or
duplicate columns. For example:

.. literalinclude:: ./support/pcsv_example_6.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

*************
Empty columns
*************

When a file has empty columns they are read as :code:`None`. Conversely
any column value that is :code:`None` is written as an empty column.
Empty columns are ones that have either an empty string (:code:`''`)
or literally no information between the column delimiters (:code:`,`)

For example, if a file ``myfile2.csv`` has the following data:

+------+-----+--------+
| Ctrl | Ref | Result |
+======+=====+========+
|    1 |   4 |     20 |
+------+-----+--------+
|    2 |     |     30 |
+------+-----+--------+
|    2 |   5 |        |
+------+-----+--------+
|      |   5 |     50 |
+------+-----+--------+

The corresponding read array is:

.. code-block:: python

        [
            ['Ctrl', 'Ref', 'Result'],
            [1, 4, 20],
            [2, None, 30],
            [2, 5, None],
            [None, 5, 50]
        ]

*********
Functions
*********

.. autofunction:: pcsv.concatenate
.. autofunction:: pcsv.dsort
.. autofunction:: pcsv.merge
.. autofunction:: pcsv.replace
.. autofunction:: pcsv.write

*****
Class
*****

.. autoclass:: pcsv.CsvFile
    :members: add_dfilter, cfilter, cols, data, dfilter, dsort, header, replace,
              reset_dfilter, rfilter, rows, write, __eq__, __repr__
    :show-inheritance:

**********************
Contracts pseudo-types
**********************

Introduction
============

The pseudo-types defined below can be used in contracts of the
`PyContracts <https://andreacensi.github.io/contracts>`_ or
`Pexdoc <http://pexdoc.readthedocs.org>`_ libraries. As an example, with the
latter:

    .. code-block:: python

        >>> from __future__ import print_function
        >>> import pexdoc
        >>> from pcsv.ptypes import csv_col_filter
        >>> @pexdoc.pcontracts.contract(cfilter='csv_col_filter')
        ... def myfunc(cfilter):
        ...     print('CSV filter received: '+cfilter)
        ...
        >>> myfunc('m')
        CSV filter received: m
        >>> myfunc(35+3j)
        Traceback (most recent call last):
            ...
        RuntimeError: Argument `cfilter` is not valid

Alternatively each pseudo-type has a :ref:`checker function <ContractCheckers>`
associated with it that can be used to verify membership. For example:

    .. code-block:: python

        >>> import pcsv.ptypes
        >>> # None is returned if object belongs to pseudo-type
        >>> pcsv.ptypes.csv_col_filter('m')
        >>> # ValueError is raised if object does not belong to pseudo-type
        >>> pcsv.ptypes.csv_col_filter(35+3j) # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: [START CONTRACT MSG: csv_col_filter]...

Description
===========

.. _CsvColFilter:

CsvColFilter
^^^^^^^^^^^^

Import as :code:`csv_col_filter`. String, integer, a list of strings or a list
of integers that identify a column or columns within a comma-separated values
(CSV) file.

Integers identify a column by position (column 0 is the leftmost column)
whereas strings identify the column by name. Columns can be identified either
by position or by name when the file has a header (first row of file
containing column labels) but only by position when the file does not have a
header.

:code:`None` indicates that no column filtering should be done

.. _CsvColSort:

CsvColSort
^^^^^^^^^^

Import as :code:`csv_col_sort`. Integer, string, dictionary or list of
integers, strings or dictionaries that specify the sort direction of a
column or columns in a comma-separated values (CSV) file.

The sort direction can be either ascending, specified by the string
:code:`'A'`, or descending, specified by the string :code:`'B'` (case
insensitive). The default sort direction is ascending.

The column can be specified numerically or with labels depending on whether the
CSV file was loaded with or without a header.

The full specification is a dictionary (or list of dictionaries if multiple
columns are to be used for sorting) where the key is the column and the value
is the sort order, thus valid examples are :code:`{'MyCol':'A'}` and
:code:`[{'MyCol':'A'}, {3:'d'}]`.

When the default direction suffices it can be omitted; for example in
:code:`[{'MyCol':'D'}, 3]`, the data is sorted first by MyCol in descending
order and then by the 4th column (column 0 is the leftmost column in a CSV
file) in ascending order

.. _CsvDataFilter:

CsvDataFilter
^^^^^^^^^^^^^

Import as :code:`csv_data_filter`. In its most general form a two-item tuple,
where one item is of `CsvColFilter`_ pseudo-type and the other item is of
`CsvRowFilter`_ pseudo-type (the order of the items is not mandated, i.e.
the first item could be of pseudo-type CsvRowFilter and the second item
could be of pseudo-type CsvColFilter or vice-versa).

The two-item tuple can be reduced to a one-item tuple when only a row or column
filter needs to be specified, or simply to an object of either CsvRowFilter
or CsvColFilter pseudo-type.

For example, all of the following are valid CsvDataFilter objects:
:code:`('MyCol', {'MyCol':2.5})`, :code:`({'MyCol':2.5}, 'MyCol')` (filter in
the column labeled MyCol and rows where the column labeled MyCol has the value
2.5), :code:`('MyCol', )` (filter in column labeled MyCol and all rows) and
:code:`{'MyCol':2.5}` (filter in all columns and only rows where the column
labeled MyCol has the values 2.5)

:code:`None`, :code:`(None, )` or :code:`(None, None)` indicate that no row or
column filtering should be done

.. _CsvFiltered:

CsvFiltered
^^^^^^^^^^^

Import as :code:`csv_filtered`. String or a boolean that indicates what type of
row and column filtering is to be performed in a comma-separated values (CSV)
file. If :code:`True`, :code:`'B'` or :code:`'b'` it indicates that both
row- and column-filtering are to be performed; if :code:`False`, :code:`'N'`
or :code:`'n'` no filtering is to be performed, if :code:`'R'` or :code:`'r'`
only row-filtering is to be performed, if :code:`'C'` or :code:`'c'` only
column-filtering is to be performed

.. _CsvRowFilter:

CsvRowFilter
^^^^^^^^^^^^

Import as :code:`csv_row_filter`. Dictionary whose elements are sub-filters
with the following structure:

* **column identifier** *(CsvColFilter)* -- Dictionary key. Column to filter
  (as it appears in the comma-separated values file header when a string is
  given) or column number (when an integer is given, column zero is the
  leftmost column)

* **value** *(list of strings or numbers, or string or number)* -- Dictionary
  value. Column value to filter if a string or number, column values to filter
  if a list of strings or numbers

If a row filter sub-filter is a column value all rows which contain the
specified value in the specified column are kept for that particular
individual filter. The overall data set is the intersection of all the data
sets specified by each individual sub-filter. For example, if the file to be
processed is:

+------+-----+--------+
| Ctrl | Ref | Result |
+======+=====+========+
|    1 |   3 |     10 |
+------+-----+--------+
|    1 |   4 |     20 |
+------+-----+--------+
|    2 |   4 |     30 |
+------+-----+--------+
|    2 |   5 |     40 |
+------+-----+--------+
|    3 |   5 |     50 |
+------+-----+--------+

Then the filter specification ``rfilter = {'Ctrl':2, 'Ref':5}`` would result
in the following filtered data set:

+------+-----+--------+
| Ctrl | Ref | Result |
+======+=====+========+
|    2 |   5 |     40 |
+------+-----+--------+

However, the filter specification ``rfilter = {'Ctrl':2, 'Ref':3}`` would
result in an empty list because the data set specified by the `Ctrl`
individual sub-filter does not overlap with the data set specified by the
`Ref` individual sub-filter.

If a row sub-filter is a list, the items of the list represent all
the values to be kept for a particular column (strings or numbers). So for
example ``rfilter = {'Ctrl':[2, 3], 'Ref':5}`` would result in the following
filtered data set:

+------+-----+--------+
| Ctrl | Ref | Result |
+======+=====+========+
|    2 |   5 |     40 |
+------+-----+--------+
|    3 |   5 |     50 |
+------+-----+--------+

:code:`None` indicates that no row filtering should be done

.. _ContractCheckers:

Checker functions
=================

.. autofunction:: pcsv.ptypes.csv_col_filter
.. autofunction:: pcsv.ptypes.csv_col_sort
.. autofunction:: pcsv.ptypes.csv_data_filter
.. autofunction:: pcsv.ptypes.csv_filtered
.. autofunction:: pcsv.ptypes.csv_row_filter
