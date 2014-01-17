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
        node.instrs.accept(self)

    def visit_DeclarationList(self, node):
        print 'DeclarationList'
        for decl in node.decls:
            curr_decl = decl.accept(self)

    def visit_Declaration(self,node):
        d_type = node.type 
        inits = node.inits.accept(self)
        for init in node.inits.inits:
            symbol = VariableSymbol(d_type, init.id)
            if self.s_table.put(symbol):
                print 'DEBUG: Added variable symbol ' + symbol.name + ' of the type ' + d_type
            else:
                print 'Symbol ' + symbol.name + ' is already defined!'

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

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'
         
    def visit_String(self, node):
        return 'string'

    def visit_FunctionDefList(self, node):
        for fundef in node.fundefs:
          fundef.accept(self)

    def visit_FunctionDef(self, node):
        
        symbol = FunctionSymbol(node.rettype, node.name, node.fmlparams)

        if self.s_table.put(symbol):
            print 'DEBUG: Added function symbol ' + symbol.name + ' with return type ' + symbol.rettype
        else:
            print 'Symbol ' + symbol.name + ' is already defined!'

        node.body.accept(self) 

    def visit_CompoundInstructions(self, node):
        node.decls.accept(self)
        node.instrs.accept(self)

    def visit_InstructionList(self, node):
        for instr in node.instrs:
            instr.accept(self)

    def visit_SimpleInstruction(self, node):
        node.expr.accept(self) 

    def visit_FunctionCall(self, node):        
        symbol = self.s_table.get(node.id)

        if type(symbol) == FunctionSymbol:
            print 'DEBUG: Captured function symbol ' + symbol.name + ' with return type ' + symbol.rettype

            actual = node.params.exprs
            formal = symbol.fmlparams.args
            if len(actual) != len(formal):
                print 'The function ' + symbol.name + ' expects ' + \
                    len(formal) + ' parameters, but ' + len(actual) + ' given!'

            for actparam, fmlparam, index in zip(actual, formal, range(1, len(actual) + 1)):
                actual_type = actparam.accept(self)
                if actual_type != fmlparam.type:
                    print 'Parameter #' + index + ' expects ' + actual_type + \
                        ', but expression of type ' + fmlparam_type + ' found'
                
        elif type(symbol) == VariableSymbol:
            print 'Symbol ' + symbol.name + ' is a variable (expected function)!'
        else:
            print 'Symbol ' + symbol.name + ' is not defined yet!'

        return symbol.rettype

