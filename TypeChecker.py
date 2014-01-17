#!/usr/bin/python

from Ttype import *
from SymbolTable import *

class TypeChecker(object):

    ttype = Ttype()
    s_table = SymbolTable('general', None)

    #sprawdza operatory: =, ==, !=, <, >
    #do skonczenia, raczej to dobry pomysl, zeby tu sprawdzac, bo w Ttype bedzie inaczje mln wierszy
    #def check_operands(self, symbol1, symbol1, operator):
    #    if symbol1.vs_type == symbol2.vs_type:
    #        return True
    #    elif (symbol1.vs_type == 'float' && symbol2.vs_type == 'int' && operator == '='):
    #        return True
    #    elif 


    def visit_Program(self, node):
        node.ext_decls.accept(self)
        node.fundefs.accept(self)
        #node.instrs.accept(self)

    def visit_DeclarationList(self, node):
        print 'DeclarationList'
        for decl in node.decls:
            curr_decl = decl.accept(self)
            print curr_decl

    def visit_Declaration(self,node):
        d_type = node.type #.accept(self)
        inits = node.inits.accept(self)
        for init in node.inits.inits:
            v_symbol = VariableSymbol(d_type, init.id)
            if self.s_table.put(v_symbol):
                print 'dodalem symbol ' + v_symbol.name + ' typu ' + d_type
                #return True
            else:
                print 'Symbol ' + v_symbol.name + ' is already defined (as ' + self.s_table.get(v_symbol.name).name + ')!'
                #return False

    def visit_BinExpr(self, node):
        type1 = node.left.accept(self)
        type2 = node.right.accept(self)
        op    = node.op
        if not (ttype.getType(op, type1, type2)):
            print 'error in BinExpr'
        
 
    def visit_RelExpr(self, node):
        type1 = node.left.accept(self);
        type2 = node.right.accept(self);
        # ...         

    def visit_Init(self, node):
        return 'Init'

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'
         
    def visit_FunctionDefList(self, node):
        for fundef in node.fundefs:
          fundef.accept(self)

    def visit_FunctionDef(self, node):
        print 'FunctionDef'

    # ... 
    # 


