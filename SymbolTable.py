#!/usr/bin/python

class Symbol(object):

    def __init__(self, name):
        self.name = name

class VariableSymbol(Symbol):

    def __init__(self, type, name):
        super(VariableSymbol, self).__init__(name)
        self.type = type

class FunctionSymbol(Symbol):

    def __init__(self, rettype, name, fmlparams):
        super(FunctionSymbol, self).__init__(name)
        self.rettype = rettype
        self.fmlparams = fmlparams

class SymbolTable(object):

    def __init__(self, parent, name):
        self.s_table_parent = parent
        self.s_table_name = name
        self.table = dict()

    def put(self, symbol):
        if not symbol.name in self.table:
            self.table[symbol.name] = symbol
            return True
        return False

    def get(self, name):
        return self.table[name]

    def getTable(self):
        return self.table

    def getParentScope(self):
        if self.parent is not None:
            return self.parent.getTable()


