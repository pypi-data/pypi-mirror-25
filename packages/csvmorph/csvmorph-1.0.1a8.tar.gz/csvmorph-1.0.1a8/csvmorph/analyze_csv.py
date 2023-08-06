from collections import namedtuple
import builtins
import csv
import gzip
import bz2
import lzma

def open(filename, compression=None, mode='rb', *args, **kwargs):
    ''' Override default open() function '''    
    open_statement = "builtins.open(filename, mode=mode, *args, **kwargs)"
    if compression:
        open_statement = open_statement.replace('builtins', compression)

    return eval(open_statement)

def analyze_csv(file, compression=None, header=0):
    '''
    Sample the first few rows of a CSV for metadata
    
    Args:
        header:     int
                    Row number of the header (zero-indexed)    
    '''
    
    results = namedtuple('CSVMeta', ['delimiter', 'quotechar', 'n_cols',
        'col_names', 'row_sample'])
    row_sample = []
    
    with open(file, compression=compression, mode='rt') as infile:
        # Sniff CSV file
        dialect = csv.Sniffer().sniff(infile.read(50000))
        
        # Get column names
        infile.seek(0)
        reader = csv.reader(infile, dialect)
        while len(row_sample) < 50:
            try:
                row_sample.append(next(reader))
            except StopIteration:
                break

    if header is not None:
        col_names = row_sample[header]
        n_cols = len(col_names)
    
    return results(delimiter=dialect.delimiter, quotechar=dialect.quotechar,
                   n_cols=n_cols, col_names=col_names, row_sample=row_sample)