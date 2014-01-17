#!/usr/bin/python

class Ttype(object):

    types = ['int', 'float', 'string']
    operators = ['+', '-', '*', '/', '%', '|', '&', '^', 'AND', 'OR', 'SHL', 'SHR']
    ttype = None

    def __init__(self): 

        self.ttype = dict((op, dict((type1, dict(dict((type2, '') for type2 in self.types))) for type1 in self.types)) for op in self.operators)
        self.ttype['+']['int']['float'] = 'float'
        self.ttype['+']['float']['int'] = 'float'
        self.ttype['+']['int']['int'] = 'int'
        self.ttype['+']['string']['string'] = 'string'
        self.ttype['+']['float']['float'] = 'float'
        self.ttype['-']['int']['float'] = 'float'
        self.ttype['-']['float']['int'] = 'float'
        self.ttype['-']['int']['int'] = 'int'
        self.ttype['-']['float']['float'] = 'float'
        self.ttype['*']['int']['float'] = 'float'
        self.ttype['*']['float']['int'] = 'float'
        self.ttype['*']['int']['int'] = 'int'
        self.ttype['*']['string']['int'] = 'string' # co tutaj ????????????
        self.ttype['*']['float']['float'] = 'float'
        self.ttype['/']['int']['float'] = 'float'
        self.ttype['/']['float']['int'] = 'float'
        self.ttype['/']['int']['int'] = 'int'
        self.ttype['/']['float']['float'] = 'float'
        #ttype[''][''][''] = ''

    def getTtype(self,op,left,right):
        return self.ttype[op][left][right]

    def getTtypeOrError(self,op,left,right):
        t = self.getTtype(op,left,right)
        return t if t else 'error'

