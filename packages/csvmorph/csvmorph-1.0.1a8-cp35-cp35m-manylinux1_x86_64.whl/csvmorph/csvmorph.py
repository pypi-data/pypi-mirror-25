'''
.. currentmodule:: csvmorph

CSVMorph
==========

.. autofunction:: to_json
.. autofunction:: stats
'''

from .parser import PyCSVReader, PyCSVStat, PyCSVCleaner
from .json import flatten_dict
from .json_streamer import PyJSONStreamer
from .helpers import process_columns, default_filename, open

from collections import defaultdict
from sys import version_info
from json import loads
import csv
import json
import os

# Handle things like segmentation faults
# (which should never happen, but it's nice to have an error message)
import faulthandler
faulthandler.enable()

def _iter_calc(reader, filename, compression, calc_func):
    # Lazily load and calculate statistics for a CSV file
    with open(filename, compression) as infile:
        data = infile.read(100000)
        while data:
            reader.feed(data)
            calc_func()
            data = infile.read(100000)
            
        reader.end_feed()
        calc_func()
        
@process_columns
@default_filename(ext='.csv')
def to_csv(filename, output, compression=None, header=0, skiplines=0,
    columns=[], _meta=None):
    '''
    to_csv(filename, output, columns=[])
    Convert a file to CSV or clean up an existing CSV file
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        output:         str
                        Output file
        header:         int
                        Line number of the header
        skiplines:      int
                        How many lines to skip
        columns:        list[str] or list[int]
                        Columns to subset
    '''
    
    if columns:
        col_names = [name for i, name in enumerate(_meta.col_names) if i in columns]
    else:
        col_names = _meta.col_names
    
    reader = PyCSVCleaner(delim=_meta.delimiter, quote=_meta.quotechar,
        header=header, subset=columns)
        
    with open(filename, compression) as infile:
        reader.feed(infile.read())
        reader.end_feed()
        
    # Write CSV
    reader.to_csv(output, quote_minimal=True, skiplines=skiplines)
    
    # Calculate statistics
    dtypes = [defaultdict(int, i) for i in reader.get_dtypes()]
    return {
        'col_names': col_names,
        'dtypes': [ {
            'None': i[0],
            'str': i[1],
            'int': i[2],
            'float': i[3]
        } for i in dtypes],
    }

@process_columns
@default_filename(ext='.json')
def to_json(filename, output=None, columns=[], _meta=None):
    '''
    to_json(filename, output=None, columns=[])
    Convert the CSV file to JSON
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        output:         str
                        Output file
        columns:        list[str] or list[int]
                        Columns to subset
    '''
    
    reader = PyCSVReader(delim=_meta.delimiter, quote=_meta.quotechar,
        col_names=_meta.col_names, subset=columns)
        
    with open(filename, mode='rb') as infile:
        reader.feed(infile.read())
        reader.end_feed()
        
    reader.to_json(output)

@process_columns
def dtypes(filename, columns=[], header=0, compression=None,
    _meta=None, **kwargs):
    '''
    Get the data types of every column in a file
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        header:         int
                        Line number of the header row
    '''
    
    reader = PyCSVStat(delim=_meta.delimiter, quote=_meta.quotechar,
        header=header, subset=columns)
    _iter_calc(reader, filename, compression, calc_func=reader.calc_dtypes)    
    dtypes = [defaultdict(int, i) for i in reader.get_dtypes()]
    return [ {'None': i[0], 'str': i[1], 'int': i[2], 'float': i[3]}
        for i in dtypes]
    
@process_columns
def stats(filename, columns=[], header=0, compression=None,
    _meta=None, **kwargs):
    '''
    stats(filename, columns)
    Get the mean, variance, and most common values for the specified values
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        header:         int
                        Line number of the header row
        columns:        list[str] or list[int]
                        Columns to calculate the mean of
    '''
    
    reader = PyCSVStat(delim=_meta.delimiter,
        quote=_meta.quotechar, 
        header=header,
        subset=columns)
    _iter_calc(reader, filename, compression, calc_func=reader.calc)
    
    if columns:
        col_names = [name for i, name in enumerate(_meta.col_names) \
            if i in columns]
    else:
        col_names = _meta.col_names
    
    means = reader.get_mean()
    vars = reader.get_variance()
    counts = reader.get_counts()
    mins = reader.get_mins()
    maxes = reader.get_maxes()
    dtypes = reader.get_dtypes()
    
    return { col_names[i]: {
        'mean': means[i],
        'variance': vars[i],
        'min': mins[i],
        'max': maxes[i],
        'dtypes': { k:v for k, v in dtypes[i].items() },
        'counts': { k:v for k, v in counts[i].items() },
    } for i in range(0, len(col_names)) }