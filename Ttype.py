#!/usr/bin/python

class Ttype(object):

	types = ['int', 'float', 'string']
	operators = ['+', '-', '*']

	ttype = None

	def __init__(self): 
		#ttype = dict((op, dict((type1, dict((type2, '') for type2 in types)) for type1 in types) for op in operators))
		self.ttype = dict((op, dict((type1, dict(dict((type2, '') for type2 in self.types))) for type1 in self.types)) for op in self.operators)
		#ttype[''][''][''] = ''
		self.ttype['+']['int']['float'] = 'float'
		self.ttype['+']['float']['int'] = 'float'
		self.ttype['+']['int']['int'] = 'int'
		self.ttype['+']['string']['string'] = 'string'
		self.ttype['+']['float']['float'] = 'float'
		#ttype[''][''][''] = ''

	def getTtype(self,op,left,right):
		return self.ttype[op][left][right]