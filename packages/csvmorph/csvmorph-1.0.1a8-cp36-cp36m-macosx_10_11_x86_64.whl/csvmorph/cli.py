from .analyze_csv import analyze_csv
from .csvmorph import to_json, json_to_csv, stats

from math import isnan

from collections import deque, OrderedDict
import click

def trim(string):
    ''' Trim a string or number to 18 characters '''
    return str(string)[:18]

@click.command()
@click.option('--columns', is_flag=True, 
    help='Print list of column names only.')
@click.argument('filename', nargs=1)
def csvpeek(filename, columns):
    info = analyze_csv(filename)
    if columns:
        for i, j in enumerate(info.col_names):
            print("[{}] '{}'".format(i, j))
    else:
        _pretty_print_ten(info)
    
def _pretty_print_ten(info):
    ''' Print first 10 rows of a CSV file + header '''
    displays = deque()
    
    # Cut up CSV file into multiple displays of 6 columns each
    for i in range(0, len(info.col_names)//6):
        try:
            displays.append({
                'col_names': info.col_names[i*6: (i+1) * 6],
                'rows': [j[i*6: (i+1) * 6] for j in info.row_sample[1:11]]
            })
        except IndexError:
            displays.append({
                'col_names': info.col_names[i*6: ],
                'rows': [j[i*6: ] for j in info.row_sample[1: \
                    min(len(info.row_sample), 11)]]
            })
            
    while displays:
        current_display = displays.popleft()
        
        print(''.join(
            '{:^20}'.format(trim(i)) for i in current_display['col_names']))
        print('-' * 20 * 6)
        
        for row in current_display['rows']:
            print(''.join('{:^20}'.format(trim(i)) for i in row))
            
        # New lines separating displays
        print('\n')
        
    print('CSV Format Information')
    print('Delimiter: {}'.format(repr(info.delimiter)))
    print('Quote Character: {}'.format(repr(info.quotechar)))

@click.command()
@click.option('--columns', default=[], help='Comma separated list of columns to subset.')
@click.argument('filename', nargs=1)
@click.option('--o', default=None, 
    help=("Specify an alternate output filename. "
          "(Default: Original filename with .csv extension)"))
def csv2json(filename, o, columns):
    if columns:
        columns = columns.split(',')
        
    to_json(filename=filename, output=o, columns=columns)
    
@click.command()
@click.option('--all', is_flag=True, help='Select all columns.')
@click.argument('filename', nargs=1)
@click.argument('columns', nargs=-1)
def csvsummary(filename, columns, all):   
    if all:
        columns = []
        
    results = stats(filename, columns=list(columns))
    
    types = {
        0: 'NULL',
        1: 'str',
        2: 'int',
        3: 'float'
    }
    
    for col, stat in results.items():
        most_common = OrderedDict(
            sorted(stat['counts'].items(), key=lambda x: x[1], reverse=True))
            
        top10 = {k:v for k,v in list(most_common.items())[:10]}

        print(col)
        
        if not isnan(stat['mean']): print("\tMean:",
            round(stat['mean'], 2))
        if not isnan(stat['variance']): print("\tVariance:",
            round(stat['variance'], 2))
        if not isnan(stat['min']): print("\tMin:",
            round(stat['min'], 2))
        if not isnan(stat['max']): print("\tMax:",
            round(stat['max'], 2))
            
        print("\tTop 10:")
        for k, v in top10.items():
            print("\t\t", k.decode('utf-8'), v)
            
        print()
        
        print("\tData Types:")
        for k, v in stat['dtypes'].items():
            print("\t\t", types[k], v)