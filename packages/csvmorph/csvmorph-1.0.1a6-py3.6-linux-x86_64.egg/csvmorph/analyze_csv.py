try:
    from statistics import mode
except ImportError:
    from collections import Counter

    def mode(list_):
        counts = Counter(list_)               
        return counts.most_common()[0][0]
    
from collections import namedtuple
import csv

def analyze_csv(file, header=None):
    '''
    Sample the first few rows of a CSV for metadata
    
    Args:
        header:     int
                    Row number of the header (zero-indexed)    
    '''
    
    results = namedtuple('CSVMeta', ['delimiter', 'quotechar', 'n_cols',
        'col_names', 'row_sample'])
    row_sample = []
    
    # Sniff CSV file
    with open(file, 'r', encoding='utf-8') as infile:
        dialect = csv.Sniffer().sniff(infile.read(50000))
        infile.seek(0)
        reader = csv.reader(infile, dialect)
        while len(row_sample) < 50:
            row_sample.append(next(reader))
            
    if header is not None:
        col_names = row_sample[header]
        n_cols = len(col_names)
    else:
        # n_cols is mode of length of 50 rows
        n_cols = mode([len(i) for i in row_sample if len(i) > 0])
        
        # Header row is first row with length = n_cols
        i = 0
        r = row_sample[0]
        while len(r) != n_cols:
            r = row_sample[i]
            i += 1
    
        col_names = row_sample[i]
    
    return results(delimiter=dialect.delimiter, quotechar=dialect.quotechar,
                   n_cols=n_cols, col_names=col_names, row_sample=row_sample)