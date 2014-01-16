#!/usr/bin/python

from Ttype import *
from SymbolTable import *

class TypeChecker(object):

    ttype = Ttype()
    s_table = SymbolTable('general', None)

    def visit_Program(self, node):
        print 'program'
        node.ext_decls.accept(self)

    def visit_DeclarationList(self, node):
        print 'DeclarationList'
        for decl in node.decls:
            decl.accept(self)

    def visit_Declaration(self,node):
        d_type = node.type#.accept(self)
        inits = node.inits.accept(self)
        for init in node.inits.inits:
            v_symbol = VariableSymbol(init.id, d_type)
            if self.s_table.put(v_symbol):
                print 'dodalem symmbol'
            else:
                print 'ten symbol juz byl zdefiniowany!'

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
        #

    def visit_Init(self, node):
        return 'Init'

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'
         
     

    # ... 
    # 


