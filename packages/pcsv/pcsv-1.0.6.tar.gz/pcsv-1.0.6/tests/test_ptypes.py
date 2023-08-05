# test_ptypes.py
# Copyright (c) 2013-2017 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,W0108

# PyPI imports
from pmisc import AE
# Intra-package imports
import pcsv.ptypes


###
# Global variables
###
emsg = lambda msg: (
    '[START CONTRACT MSG: {0}]Argument `*[argument_name]*` '
    'is not valid[STOP CONTRACT MSG]'.format(msg)
)


###
# Helper functions
###
def check_contract(obj, name, value):
    AE(obj, ValueError, emsg(name), obj=value)


###
# Test functions
###
def test_csv_col_filter_contract():
    """ Test CsvColFilter pseudo-type """
    items = [True, 1.0, [], [1, True, 3], ['a', 'b', True]]
    for item in items:
        check_contract(pcsv.ptypes.csv_col_filter, 'csv_col_filter', item)
    items = [None, 1, 'a', [1, 2], ['a']]
    for item in items:
        pcsv.ptypes.csv_col_filter(item)


def test_csv_col_sort_contract():
    """ Test CsvColSort pseudo-type """
    items = [
        True, None, ['a', None], {(1, 2):'A'}, {'a':True}, {0:'hello'}, []
    ]
    for item in items:
        check_contract(pcsv.ptypes.csv_col_sort, 'csv_col_sort', item)
    items = [
        1,
        'a',
        {'a':'D'},
        {0:'d'},
        {1:'a'},
        [1, 'a'],
        [1, 'a', {'b':'d'}, {0:'A'}]
    ]
    for item in items:
        pcsv.ptypes.csv_col_sort(item)


def test_csv_data_filter_contract():
    """ Test CsvDataFilter pseudo-type """
    items = [
        True,
        (1, 2, 3),
        (True, 'A'),
        (True, ),
        (None, True),
        ('A', 'A'),
        ({'B':1}, {'C':5}),
        {2.0:5},
        ({2.0:5}, 'A'),
        (['A', True], {'A':1}),
        ('A', {}),
        ([], {'A':1}),
        ({}, []),
        {'dfilter':{'a':{'xx':2}}},
        {'dfilter':{'a':[3, {'xx':2}]}}
    ]
    for item in items:
        check_contract(pcsv.ptypes.csv_data_filter, 'csv_data_filter', item)
    items = [
        None,
        (None, ),
        (None, None),
        1,
        'A',
        ['B', 1],
        {'A':1},
        {'A':1, 'B':2}
    ]
    for item in items:
        pcsv.ptypes.csv_data_filter(item)


def test_csv_filtered_contract():
    """ Test CsvFiltered pseudo-type """
    for item in [5, 'BC']:
        check_contract(pcsv.ptypes.csv_filtered, 'csv_filtered', item)
    for item in [True, False, 'B', 'b', 'C', 'c', 'R', 'r', 'N', 'n']:
        pcsv.ptypes.csv_filtered(item)


def test_csv_row_filter_contract():
    """ Test CsvRowFilter pseudo-type """
    items = [
        'a',
        {5.0:10},
        {'a':{'xx':2}},
        {'a':[3, {'xx':2}]},
        {'b':True}
    ]
    for item in items:
        check_contract(pcsv.ptypes.csv_row_filter, 'csv_row_filter', item)
    exmsg = (
        '[START CONTRACT MSG: csv_row_filter]Argument '
        '`*[argument_name]*` is empty[STOP CONTRACT MSG]'
    )
    AE(pcsv.ptypes.csv_row_filter, ValueError, exmsg, obj={})
    items = [None, {'x':5}]
    for item in items:
        pcsv.ptypes.csv_row_filter(item)
