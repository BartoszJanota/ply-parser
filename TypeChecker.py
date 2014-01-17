#!/usr/bin/python

from Ttype import *
from SymbolTable import *

class TypeChecker(object):


    def __init__(self):
        self.ttype = Ttype()
        self.s_table = SymbolTable('general', None)

    #sprawdza operatory: =, ==, !=, <, >
    #do skonczenia, raczej to dobry pomysl, zeby tu sprawdzac, bo w Ttype bedzie inaczje mln wierszy
    #def check_operands(self, symbol1, symbol1, operator):
    #    if symbol1.vs_type == symbol2.vs_type:
    #        return True
    #    elif (symbol1.vs_type == 'float' && symbol2.vs_type == 'int' && operator == '='):
    #        return True
    #    elif 


    def visit_Program(self, node):
        #print('Program appeared at line %s' % node.lineno)
        node.ext_decls.accept(self)
        node.fundefs.accept(self)
        node.instrs.accept(self)


    def visit_DeclarationList(self, node):
        for decl in node.decls:
            curr_decl = decl.accept(self)


    def visit_Declaration(self,node):

        d_type = node.type 
        inits = node.inits.accept(self)
        for init in node.inits.inits:
            symbol = VariableSymbol(d_type, init.id)
            if not self.s_table.put(symbol):
                print 'Symbol ' + symbol.name + ' is already defined!'
            #else:
                #print 'DEBUG: Added variable symbol ' + symbol.name + ' of the type ' + d_type


    def visit_BinExpr(self, node):
        type1 = node.left.accept(self)
        type2 = node.right.accept(self)
        if type1 == 'error' or type2 == 'error':
            return 'error'

        op = node.op

        result_type = self.ttype.getTtypeOrError(op, type1, type2)
        #print 'DEBUG: Captured expression ' + type1 + ' ' + op + ' ' + type2 + \
            #', the result type is ' + result_type
            
        return result_type 
        
 
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


    def visit_Variable(self, node):
        
        symbol = self.s_table.get(node.id)

        if type(symbol) == VariableSymbol:
            #print 'DEBUG: Captured variable symbol ' + symbol.name + ' of type ' + symbol.type
            return symbol.type

        elif type(symbol) == FunctionSymbol:
            print 'Symbol ' + symbol.name + ' is a function (expected variable)!'
            return 'error'

        else: # symbol == None
            print 'Variable ' + node.id + ' is undefined!'
            return 'error'


    def visit_FunctionDefList(self, node):
    
        for fundef in node.fundefs:
          fundef.accept(self)


    def visit_FunctionDef(self, node):
        
        symbol = FunctionSymbol(node.rettype, node.name, node.fmlparams)

        if not self.s_table.put(symbol):
            print 'Symbol ' + symbol.name + ' is already defined!'
        #else:
            #print 'DEBUG: Added function symbol ' + symbol.name + ' with return type ' + symbol.rettype

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
            #print 'DEBUG: Captured function symbol ' + symbol.name + ' with return type ' + symbol.rettype

            actual = node.params.exprs
            actual_types = [actparam.accept(self) for actparam in actual]
            formal = symbol.fmlparams.args
            formal_types = [fmlparam.type for fmlparam in formal]

            if 'error' in actual_types: return 'error'

            if len(actual) != len(formal):
                print 'The function ' + symbol.name + ' expects ' + \
                    str(len(formal)) + ' parameters, but ' + str(len(actual)) + ' given!'
                return 'error'

            for actual_type, formal_type, index in zip(actual_types, formal_types, range(1, len(actual) + 1)):
                if actual_type != formal_type:
                    print 'Parameter #' + str(index) + ' expects ' + formal_type + \
                        ', but expression of type ' + actual_type + ' found'
                    return 'error'

            return symbol.rettype
                
        elif type(symbol) == VariableSymbol:

            print 'Symbol ' + symbol.name + ' is a variable (expected function)!'
            return 'error'

        else: # symbol == None

            print 'Function ' + node.id + ' is undefined!'
            return 'error'




