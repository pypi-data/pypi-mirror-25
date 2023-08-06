# Helper Functions for csvmorph.py

from functools import wraps
from collections import Iterable
from .analyze_csv import analyze_csv, open

def default_filename(ext):
    ''' Provide a default filename '''
    
    def decorator(func):
        @wraps(func)
        def inner(filename, output=None, *args, **kwargs):
            if not output:
                output = ''.join(filename.split('.')[:-1]) + ext
                
            return func(filename=filename, output=output, *args, **kwargs)
        return inner
    return decorator

def process_columns(func):
    ''' Convert the "columns" argument into a list of integer indices '''

    @wraps(func)
    def inner(filename, *args, header=None, compression=None,
        columns=[], **kwargs):
        if header:
            meta = analyze_csv(filename, compression=compression,
                header=header)
        else:
            meta = analyze_csv(filename, compression=compression)
            
        kwargs['_meta'] = meta
        
        if columns:
            # Assert columns is a list or tuple
            if not isinstance(columns, Iterable):
                raise ValueError('"columns" must be a list of column names '
                                 'or indices.')
        
            # Convert column string names to integer indices
            for i, cname in enumerate(columns):
                try:
                    columns[i] = int(cname)
                except ValueError:
                    if cname not in meta.col_names:
                        raise ValueError("Couldn't find a column named {} from {}".format(
                            cname, meta.col_names))
                    else:
                        columns[i] = meta.col_names.index(columns[i])
        
        return func(filename=filename, columns=columns,
            compression=compression, *args, **kwargs)
    return inner