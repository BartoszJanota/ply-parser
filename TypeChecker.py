#!/usr/bin/python

from Ttype import *
from SymbolTable import *

class TypeChecker(object):


    def __init__(self):
        self.ttype = Ttype()


    def handle_error(self, pos, msg):
        print 'Line ' + str(pos.line) + ': ' + msg


    def visit_Program(self, node, table):
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
                self.handle_error(node.pos, 'Symbol ' + symbol.name + ' is already defined')
            #else:
                #print 'DEBUG: Added variable symbol ' + symbol.name + ' of the type ' + d_type


    def visit_BinExpr(self, node, table):
        type1 = node.left.accept(self, table)
        type2 = node.right.accept(self, table)
        if type1 == 'error' or type2 == 'error':
            return 'error'

        op = node.op

        result_type = self.ttype.getTtypeOrError(op, type1, type2)
        if result_type == 'error':
            self.handle_error(node.pos, 'Error: Left ' + type1 + ' operand and right ' + type2 + ' operand are not allowed for \'' + op + '\' operator.')
            return 'error'
        #print 'DEBUG: Captured expression ' + type1 + ' ' + op + ' ' + type2 + \
        #    ', the result type is ' + result_type
            
        return result_type 
        
 
    def visit_ChoiceInstruction(self, node, table):
        cond_type = node.cond.accept(self, table);
        ithen = node.ithen.accept(self, SymbolTable(table, 'ithen'));
        ielse = None
        if node.ielse is not None:
            ielse = node.ielse.accept(self, SymbolTable(table, 'ielse'));

    def visit_WhileInstruction(self, node, table):
        cond_type = node.cond.accept(self, table);
        instr = node.instr.accept(self, SymbolTable(table, 'while'));

    def visit_RepeatInstruction(self, node, table):
        cond_type = node.cond.accept(self, table);
        instrs = node.instrs.accept(self, SymbolTable(table, 'repeat'));

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
            self.handle_error(node.pos, 'Symbol ' + symbol.name + ' is a function (expected a variable)')
            return 'error'

        else: # symbol == None
            self.handle_error(node.pos, 'Symbol ' + node.id + ' is undefined')
            return 'error'


    def visit_FunctionDefList(self, node, table):
    
        for fundef in node.fundefs:
          fundef.accept(self, table)


    def visit_FunctionDef(self, node, table):
        
        symbol = FunctionSymbol(node.rettype, node.name, node.fmlparams)

        if not table.put(symbol):
            self.handle_error(node.pos, 'Symbol ' + symbol.name + ' is already defined')
        #else:
            #print 'DEBUG: Added function symbol ' + symbol.name + ' with return type ' + symbol.rettype

        subtable = SymbolTable(table, symbol)
        for fmlparam in node.fmlparams.args:
            type = fmlparam.type
            id = fmlparam.id
            symbol = VariableSymbol(type, id)
            if not subtable.put(symbol):
                self.handle_error(node.pos, 'Parameter ' + id + ' already declared')

        node.body.accept(self, subtable)


    def visit_CompoundInstructions(self, node, table):

        subtable = SymbolTable(table, table.function)
        node.decls.accept(self, subtable)
        node.instrs.accept(self, subtable)


    def visit_InstructionList(self, node, table):
        for instr in node.instrs:
            instr.accept(self, table)


    def visit_PrintInstruction(self, node, table):
        node.expr.accept(self, table) 

    def visit_ReturnInstruction(self, node, table):

        if table.function:

            rettype = node.expr.accept(self, table)
            if rettype != 'error':
                expected_rettype = table.function.rettype
                if rettype != expected_rettype:
                    self.handle_error(node.pos, 'Wrong return expression type, expected ' +\
                        expected_rettype + ', given ' + rettype)

        else: # global scope
            self.handle_error(node.pos, 'Return statement used outside a function')

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
                self.handle_error(node.pos, 'The function ' + symbol.name + ' expects ' + \
                    str(len(formal)) + ' parameters, but ' + str(len(actual)) + ' given')
                return 'error'

            for actual_type, formal_type, index in zip(actual_types, formal_types, range(1, len(actual) + 1)):
                if actual_type != formal_type and not (actual_type == 'int' and formal_type == 'float'):
                    self.handle_error(node.pos, 'Parameter #' + str(index) + ' expects ' + formal_type + \
                        ', but expression of type ' + actual_type + ' found')
                    return 'error'

            return symbol.rettype
                
        elif type(symbol) == VariableSymbol:

            self.handle_error(node.pos, 'Symbol ' + symbol.name + ' is a variable (expected function)')
            return 'error'

        else: # symbol == None

            self.handle_error(node.pos, 'Function ' + node.id + ' is undefined')
            return 'error'

    def visit_Assignment(self, node, table):
        
        lhs_type = table.get(node.id)
        if lhs_type: lhs_type = lhs_type.type
        rhs_type = node.expr.accept(self, table)

        if lhs_type == None:
            self.handle_error(node.pos, 'Variable ' + node.id + ' to be assigned is unknown')

        elif rhs_type == 'error':
            pass

        elif not self.check_assignment(lhs_type, rhs_type):
            art1 = 'a' if str(lhs_type) == 'int' else 'an'
            art2 = 'a' if str(rhs_type) == 'int' else 'an'
            self.handle_error(node.pos, 'Cannot assign ' + art1 + ' ' + str(rhs_type) +\
                ' to ' + art2 + ' ' + str(lhs_type) + ' variable')


    def check_assignment(self, oper1_type, oper2_type):
        if oper1_type == oper2_type:
            return True
        elif oper1_type == 'float' and oper2_type == 'int':
            return True
        else:
            return False



