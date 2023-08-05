'''
.. currentmodule:: csvmorph

CSVMorph
==========

.. autofunction:: to_json
.. autofunction:: mean
'''

from .analyze_csv import analyze_csv
from .parser import PyCSVReader, PyCSVStat
from .json import flatten_dict
from .json_streamer import PyJSONStreamer
from .helpers import process_columns, default_filename

from sys import version_info
from json import loads
import gzip
import bz2
import lzma
import csv
import json
import os

import faulthandler
faulthandler.enable()

PYTHON_VERSION = version_info.major + version_info.minor * 0.1

# Deserializing JSON from binary is not supported until 3.6
if PYTHON_VERSION < 3.6:
    def loads(s, *args, **kwargs):
        return json.loads(s.decode('utf-8'), *args, **kwargs)

def _decompress_or_open(filename, compression):
    open_statement = "open(filename, mode='rb')"
    if compression:
        open_statement = compression + "." + open_statement
    
    return eval(open_statement)
        
@process_columns
@default_filename(ext='.csv')
def to_csv(filename, output, columns=[], _meta=None):
    '''
    to_csv(filename, output, columns=[])
    Convert a file to CSV or clean up an existing CSV file
    
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
        
    with _decompress_or_open(filename, compression) as infile:
        reader.feed(infile.read())
        reader.end_feed()
        
    reader.to_csv(output)

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
    
    
    if not columns:
        columns = list(range(0, len(_meta.col_names)))
    
    reader = PyCSVReader(delim=_meta.delimiter, quote=_meta.quotechar,
        col_names=_meta.col_names, subset=columns)
        
    with open(filename, mode='rb') as infile:
        reader.feed(infile.read())
        reader.end_feed()
        
    reader.to_json(output)
    
@default_filename(ext='.csv')
def json_to_csv(filename, output=None, delim=',', 
    recsep='\r\n', compression=None):
    '''
    Flatten a JSON and convert it to CSV
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        output:         str
                        Output file
        delim:          str (default: comma)
                        Delimiter for output CSV
        recsep:         str (default: line carriage line feed "\r\n")
                         * Record separator for output CSV
                         * Tip: Use "\n" for Microsoft Excel
        compression:    str (default: None)
                        Compression algorithm ('gzip', 'bz2', or 'lzma')
    '''
    
    with _decompress_or_open(filename, compression) as infile, \
        open(output, mode='w') as outfile:
        writer = csv.writer(outfile, delimiter=delim, lineterminator=recsep)
        streamer = PyJSONStreamer()

        while True:
            data = infile.read(1000000)
            if not data: break
            
            streamer.feed(data)
            
        # Write buffer to CSV
        rows = [loads(i, object_hook=flatten_dict) for i in streamer]
        
        # Get column names
        keys = set()
        for dict_ in rows:
            keys = keys.union(set(dict_.keys()))
        
        # Write column names
        col_names = list(keys)
        writer.writerow(col_names)
        
        for i in rows:
            writer.writerow([i[col] for col in col_names])
    
@process_columns
def dtypes(filename, _meta=None, **kwargs):
    '''
    Get the data types of every column in a file
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
    '''
    
    reader = PyCSVStat(delim=_meta.delimiter,
        quote=_meta.quotechar, 
        col_names=_meta.col_names,
        subset=list(range(0, len(_meta.col_names))))

    with open(filename, mode='rb') as infile:
        reader.feed(infile.read())
        reader.end_feed()

    reader.calc_dtypes()
    dtypes = reader.get_dtypes()

    return dtypes
    
@process_columns
def stats(filename, columns=None, _meta=None, **kwargs):
    '''
    stats(filename, columns)
    Get the mean, variance, and most common values for the specified values
    
    Args:
        filename:       str or os.path
                        CSV file to be converted
        columns:        list[str] or list[int]
                        Columns to calculate the mean of
    '''
    
    if not columns:
        columns = list(range(0, len(_meta.col_names)))
        
    reader = PyCSVStat(delim=_meta.delimiter,
        quote=_meta.quotechar, 
        col_names=_meta.col_names,
        subset=columns)

    with open(filename, mode='rb') as infile:
        reader.feed(infile.read())
        reader.end_feed()
        
    # filename = os.path.join(os.getcwd(), filename)
        
    # reader.read_csv(filename)
    reader.calc()
        
    means = reader.get_mean()
    vars = reader.get_variance()
    counts = reader.get_counts()
    mins = reader.get_mins()
    maxes = reader.get_maxes()
    dtypes = reader.get_dtypes()

    return { _meta.col_names[columns[i]]: {
        'mean': means[i],
        'variance': vars[i],
        'min': mins[i],
        'max': maxes[i],
        'dtypes': { k:v for k, v in dtypes[i].items() },
        'counts': { k:v for k, v in counts[i].items() },
    } for i in range(0, len(columns)) }