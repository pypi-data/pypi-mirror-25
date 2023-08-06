from os import path

# Get data from test directory
PARENT_DIR = path.split(path.dirname(__file__))[:-1]
DATA = path.join(PARENT_DIR[0], 'tests', 'data')
FAKE_DATA = path.join(DATA, 'fake_data')
REAL_DATA = path.join(DATA, 'real_data')
MIMESIS_DATA = path.join(DATA, 'mimesis_data')