#!/usr/bin/python

class Ttype(object):

    types = ['int', 'float', 'string']
    operators = ['+', '-', '*', '/', '%', '|', '&', '^', '&&', '||', '<<', '>>', '<' , '>', '==', '!=', '>=', '<=']
    ttype = None

    def __init__(self): 

        self.ttype = dict((op, dict((type1, dict(dict((type2, '') for type2 in self.types))) for type1 in self.types)) for op in self.operators)

        self.populateArithmetic()
        self.ttype['+']['string']['string'] = 'string'
        self.ttype['*']['string']['int'] = 'string'

        self.populateLogicalAndShifts()

        self.populateComparisons()


    def populateArithmetic(self):

        for op in '+-*/%':
            self.ttype[op]['int']['float'] = 'float'
            self.ttype[op]['float']['int'] = 'float'
            self.ttype[op]['int']['int'] = 'int'
            self.ttype[op]['float']['float'] = 'float'
        
    def populateLogicalAndShifts(self):
     
        for op in '&', '^', '|', '&&', '||', '>>', '<<':
            self.ttype[op]['int']['int'] = 'int'
       
    def populateComparisons(self):

        for op in '<', '>', '==', '!=', '<=', '>=':
          self.ttype[op]['int']['int'] = 'int'
          self.ttype[op]['int']['float'] = 'int'
          self.ttype[op]['float']['int'] = 'int'
          self.ttype[op]['float']['float'] = 'int'
          self.ttype[op]['string']['string'] = 'int'

    def getTtype(self,op,left,right):
        return self.ttype[op][left][right]

    def getTtypeOrError(self,op,left,right):
        t = self.getTtype(op,left,right)
        return t if t else 'error'

