from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "csv-parser/src/json_streamer.hpp" namespace "csvmorph":
    cdef cppclass JSONStreamer:
        JSONStreamer() except +
        void feed(string)
        string pop()
        bool empty()
        
cdef class PyJSONStreamer:
    cdef JSONStreamer* c_streamer
    
    def __cinit__(self):
        self.c_streamer = new JSONStreamer()
        
    def feed(self, string):
        self.c_streamer.feed(string)
        
    def pop(self):
        return self.c_streamer.pop()
        
    def empty(self):
        return self.c_streamer.empty()
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if not self.c_streamer.empty():
            return self.c_streamer.pop()
        else:
            raise StopIteration
        
    def __dealloc__(self):
        del self.c_streamer