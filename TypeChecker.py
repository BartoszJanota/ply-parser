#!/usr/bin/python

from Ttype import *
from SymbolTable import *

class TypeChecker(object):


    def __init__(self):
        self.ttype = Ttype()

    def visit_Program(self, node, table):
        #print('Program appeared at line %s' % node.lineno)
        table = SymbolTable(None, None)
        node.ext_decls.accept(self, table)
        node.fundefs.accept(self, table)
        node.instrs.accept(self, table)


    def visit_DeclarationList(self, node, table):
        for decl in node.decls:
            curr_decl = decl.accept(self, table)


    def visit_Declaration(self, node, table):

        d_type = node.type 
        inits = node.inits.accept(self, table)
        for init in node.inits.inits:
            symbol = VariableSymbol(d_type, init.id)
            if not table.put(symbol):
                print 'Symbol ' + symbol.name + ' is already defined!'
            #else:
                #print 'DEBUG: Added variable symbol ' + symbol.name + ' of the type ' + d_type


    def visit_BinExpr(self, node, table):
        type1 = node.left.accept(self, table)
        type2 = node.right.accept(self, table)
        if type1 == 'error' or type2 == 'error':
            return 'error'

        op = node.op

        result_type = self.ttype.getTtypeOrError(op, type1, type2)
        #print 'DEBUG: Captured expression ' + type1 + ' ' + op + ' ' + type2 + \
        #    ', the result type is ' + result_type
            
        return result_type 
        
 
    def visit_RelExpr(self, node, table):
        type1 = node.left.accept(self, table);
        type2 = node.right.accept(self, table);
        # ...         


    def visit_Integer(self, node, table):
        return 'int'


    def visit_Float(self, node, table):
        return 'float'


    def visit_String(self, node, table):
        return 'string'


    def visit_Variable(self, node, table):
        
        symbol = table.get(node.id)

        if type(symbol) == VariableSymbol:
            #print 'DEBUG: Captured variable symbol ' + symbol.name + ' of type ' + symbol.type
            return symbol.type

        elif type(symbol) == FunctionSymbol:
            print 'Symbol ' + symbol.name + ' is a function (expected variable)!'
            return 'error'

        else: # symbol == None
            print 'Variable ' + node.id + ' is undefined!'
            return 'error'


    def visit_FunctionDefList(self, node, table):
    
        for fundef in node.fundefs:
          fundef.accept(self, table)


    def visit_FunctionDef(self, node, table):
        
        symbol = FunctionSymbol(node.rettype, node.name, node.fmlparams)

        if not table.put(symbol):
            print 'Symbol ' + symbol.name + ' is already defined!'
        #else:
            #print 'DEBUG: Added function symbol ' + symbol.name + ' with return type ' + symbol.rettype

        node.body.accept(self, SymbolTable(table, symbol))


    def visit_CompoundInstructions(self, node, table):
        node.decls.accept(self, table)
        node.instrs.accept(self, table)


    def visit_InstructionList(self, node, table):
        for instr in node.instrs:
            instr.accept(self, table)
            #print "DEBUG: Captured simple instr " +  str(instr)


    def visit_SimpleInstruction(self, node, table):
        node.expr.accept(self, table) 

    def visit_ReturnInstruction(self, node, table):

        if table.function:

            rettype = node.expr.accept(self, table)
            if rettype != 'error':
                expected_rettype = table.function.rettype
                if rettype != expected_rettype:
                    print 'Wrong return expression type, expected ' + expected_rettype + \
                        ', given ' + rettype

        else: # global scope
          print 'Return statement used outside a function!'

    def visit_FunctionCall(self, node, table):        
        symbol = table.get(node.id)

        if type(symbol) == FunctionSymbol:
            #print 'DEBUG: Captured function symbol ' + symbol.name + ' with return type ' + symbol.rettype

            actual = node.params.exprs
            actual_types = [actparam.accept(self, table) for actparam in actual]
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

    def visit_Assignment(self, node, table):
        oper1_type = node.expr1.accept(self, table)
        oper2_type = node.expr2.accept(self, table)
        if oper1_type == 'error' or oper2_type == 'error':
            return 'error'
        if not self.check_assignment(oper1_type, oper2_type):
            art1 = 'a' if str(oper1_type) == 'int' else 'an'
            art2 = 'a' if str(oper2_type) == 'int' else 'an'
            print 'Cannot assign ' + art1 + ' ' + str(oper2_type) + ' operand to ' + art2 + ' ' + str(oper1_type) + ' operand.'
        return True    
        #print 'DEBUG: Captured assingment ' + str(node.expr1) + ' = ' + str(node.expr2)


    def check_assignment(self, oper1_type, oper2_type):
        if oper1_type == oper2_type:
            return True
        elif oper1_type == 'float' and oper2_type == 'int':
            return True
        else:
            return False

    # def check_operands(self, symbol1, symbol2, operator):
    #    if symbol1.vs_type == symbol2.vs_type:
    #        return True
    #    elif (symbol1.vs_type == 'float' and symbol2.vs_type == 'int' and operator == '='):
    #        return True
    #    else:
    #         return True





