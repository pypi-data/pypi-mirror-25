from cython.operator cimport dereference as deref
from libc.math cimport isnan
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.map cimport map
from libcpp.string cimport string

cdef extern from "csv-parser/src/csv_stat.hpp" namespace "csvmorph":
    cdef cppclass CSVReader:
        CSVReader(string, string, int, vector[int]) except +
        void feed(string),
        void end_feed(),
        void read_csv(string),
        void to_csv(string),
        void to_json(string),
        vector[string] pop(),
        bool empty()
        
    cdef cppclass CSVStat(CSVReader):
        CSVStat(string, string, int, vector[int]) except +
        void calc(bool, bool, bool) except + 
        vector[long double] get_mean()
        vector[long double] get_variance()
        vector[long double] get_mins()
        vector[long double] get_maxes()
        vector[map[string, int]] get_counts()
        vector[map[int, int]] get_dtypes()
        
cdef class PyCSVReader:
    cdef CSVReader* c_reader
    
    def __cinit__(self, delim, quote, header, subset=[]):
        cdef string delim_ = delim.encode('utf-8')
        cdef string quote_ = quote.encode('utf-8')
        self.c_reader = new CSVReader(delim_, quote_, header, subset)
    
    def feed(self, input):
        ''' Input should be a bytes object '''
        self.c_reader.feed(input)
        
    def end_feed(self):
        self.c_reader.end_feed()
        
    def pop(self):
        return self.c_reader.pop()
        
    def empty(self):
        return self.c_reader.empty()
        
    def read_csv(self, filename):
        cdef string filename_ = filename.encode('utf-8')
        self.c_reader.read_csv(filename_)
        
    def to_csv(self, filename):
        cdef string filename_ = filename.encode('utf-8')
        self.c_reader.to_csv(filename_)
        
    def to_json(self, filename):
        cdef string filename_ = filename.encode('utf-8')
        self.c_reader.to_json(filename_)
    
    def __dealloc__(self):
        del self.c_reader
        
cdef class PyCSVStat(PyCSVReader):
    cdef CSVStat* c_stat
    
    def __cinit__(self, delim, quote, header, subset=[]):
        cdef string delim_ = delim.encode('utf-8')
        cdef string quote_ = quote.encode('utf-8')
        self.c_stat = new CSVStat(delim_, quote_,header, subset)
    
    def read_csv(self, filename):
        cdef string filename_ = filename.encode('utf-8')
        self.c_stat.read_csv(filename_)
    
    def feed(self, input):
        ''' Input should be a bytes object '''
        self.c_stat.feed(input)
        
    def end_feed(self):
        self.c_stat.end_feed()
    
    def calc(self):
        self.c_stat.calc(True, True, True)
        
    def calc_dtypes(self):
        ''' Only get data type count '''
        self.c_stat.calc(False, False, True)
    
    def get_mean(self):
        return self.c_stat.get_mean()
    
    def get_variance(self):
        return self.c_stat.get_variance()
        
    def get_mins(self):
        return self.c_stat.get_mins()
        
    def get_maxes(self):
        return self.c_stat.get_maxes()
        
    def get_counts(self):
        return self.c_stat.get_counts()
        
    def get_dtypes(self):
        return self.c_stat.get_dtypes()
    
    def __dealloc__(self):
        del self.c_stat