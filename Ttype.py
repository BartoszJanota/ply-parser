#!/usr/bin/python

class Ttype(object):

    types = ['int', 'float', 'string']
    operators = ['+', '-', '*', '/', '%', '|', '&', '^', 'AND', 'OR', 'SHL', 'SHR', '<' , '>', '==', '!=', 'GE', 'LE']
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
        # self.ttype['/'][''][''] = ''
        # self.ttype['%'][''][''] = ''
        # self.ttype['|'][''][''] = ''
        # self.ttype['&'][''][''] = ''
        # self.ttype['^'][''][''] = ''
        # self.ttype['AND'][''][''] = ''
        # self.ttype['OR'][''][''] = ''
        # self.ttype['SHL'][''][''] = ''
        # self.ttype['SHR'][''][''] = ''
        self.ttype['<']['int']['int'] = 'int'
        self.ttype['<']['int']['float'] = 'int'
        self.ttype['<']['float']['int'] = 'int'
        self.ttype['<']['float']['int'] = 'int'
        self.ttype['<']['float']['float'] = 'int'
        self.ttype['<']['string']['string'] = 'int'
        self.ttype['>']['int']['int'] = 'int'
        self.ttype['>']['int']['float'] = 'int'
        self.ttype['>']['float']['int'] = 'int'
        self.ttype['>']['float']['int'] = 'int'
        self.ttype['>']['float']['float'] = 'int'
        self.ttype['>']['string']['string'] = 'int'
        self.ttype['==']['int']['int'] = 'int'
        self.ttype['==']['int']['float'] = 'int'
        self.ttype['==']['float']['int'] = 'int'
        self.ttype['==']['float']['int'] = 'int'
        self.ttype['==']['float']['float'] = 'int'
        self.ttype['==']['string']['string'] = 'int'
        self.ttype['!=']['int']['int'] = 'int'
        self.ttype['!=']['int']['float'] = 'int'
        self.ttype['!=']['float']['int'] = 'int'
        self.ttype['!=']['float']['int'] = 'int'
        self.ttype['!=']['float']['float'] = 'int'
        self.ttype['!=']['string']['string'] = 'int'
        self.ttype['LE']['int']['int'] = 'int'
        self.ttype['LE']['int']['float'] = 'int'
        self.ttype['LE']['float']['int'] = 'int'
        self.ttype['LE']['float']['int'] = 'int'
        self.ttype['LE']['float']['float'] = 'int'
        self.ttype['LE']['string']['string'] = 'int'
        self.ttype['GE']['int']['int'] = 'int'
        self.ttype['GE']['int']['float'] = 'int'
        self.ttype['GE']['float']['int'] = 'int'
        self.ttype['GE']['float']['int'] = 'int'
        self.ttype['GE']['float']['float'] = 'int'
        self.ttype['GE']['string']['string'] = 'int'


    def getTtype(self,op,left,right):
        return self.ttype[op][left][right]

    def getTtypeOrError(self,op,left,right):
        t = self.getTtype(op,left,right)
        return t if t else 'error'

