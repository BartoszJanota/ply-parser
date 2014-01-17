#!/usr/bin/python


class VariableSymbol(object):

    vs_name = ''
    vs_type = ''

    def __init__(self, vs_name, vs_type):
        self.vs_type = vs_type
        self.vs_name = vs_name


class SymbolTable(object):

    s_table_name = ''
    s_table_parent = ''
    table = dict()

    def __init__(self, parent, name):
        self.s_table_parent = parent
        self.s_table_name = name

    def put(self, symbol):
        if not symbol.vs_name in self.table:
            self.table[symbol.vs_name] = symbol.vs_type
            return True
        return False

    def get(self, name):
        return self.table[name]

    def getTable(self):
        return self.table

    def getParentScope(self):
        if self.parent is not None:
            return self.parent.getTable()





