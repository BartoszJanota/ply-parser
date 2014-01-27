
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):

    class BreakException(Exception):
        pass

    class ContinueException(Exception):
        pass

    def __init__(self):
        self.globalMemory = MemoryStack(Memory("globalMemory"))
        self.functionMemory = MemoryStack(Memory("functionMemory"))
        self.precompile_operators()

    @on('node')
    def visit(self, node):
        pass

    def action_lambda(self, op):
        return eval('lambda x, y: x ' + op + ' y')

    def precompile_operators(self):
        self.actions = {}
        operators = [c for c in "<>+-*/%&|^"] + ['<=', '>=', '==', '!=', '<<', '>>']

        for op in operators:
            self.actions[op] = self.action_lambda(op)

        self.actions['&&'] = self.action_lambda('and')
        self.actions['||'] = self.action_lambda('or')

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.iaccept(self)
        r2 = node.right.iaccept(self)

        return self.actions[node.op](r1, r2)


    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.WhileInstruction)
    def visit(self, node):

        try:
          while node.cond.iaccept(self):
              try:
                  node.instr.iaccept(self)
              except ContinueException:
                  pass
        except BreakException:
            pass

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException        

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException

    @when(AST.Program)
    def visit(self, node):
        node.ext_decls.iaccept(self)
        node.fundefs.iaccept(self)
        node.instrs.iaccept(self)
    
    @when(AST.InstructionList)
    def visit(self, node):
        for instr in node.instrs:
            instr.iaccept(self)

    @when(AST.CompoundInstructions)
    def visit(self, node):
        #to jest do naprawy!!
        #bo jak zadeklarujesz cos to sie ma odlozyc na lokalnym stosie
        node.decls.iaccept(self)
        node.instrs.iaccept(self)


    @when(AST.PrintInstruction)
    def visit(self, node):
        print node.expr.iaccept(self)

    @when(AST.Variable)
    def visit(self, node):
        #
        #
        # nie wiem dlaczego ten visit zwraca liste ??
        #
        #
        #print node.id
        variable = self.functionMemory.get(node.id)
        if variable is not None:
            #print variable
            return variable
        else:
            variable = self.globalMemory.get(node.id)
            if variable is not None:
                #print variable
                return variable
        return variable

    @when(AST.DeclarationList)
    def visit(self, node):
        for decl in node.decls:
            decl.iaccept(self)

    @when(AST.Declaration)
    def visit(self, node, table = None): 
        node.inits.iaccept(self)

    @when(AST.InitList)
    def visit(self, node):
        for init in node.inits:
            init.iaccept(self)

    @when(AST.Init)
    def visit(self, node):
        val = node.expr.iaccept(self)
        self.globalMemory.put(node.id, val)

    @when(AST.Assignment)
    def visit(self, node):
        r2 = node.expr.iaccept(self)
        if r2 is not None:
            if self.functionMemory.get(node.id) is not None:
                self.functionMemory.put(node.id, r2)
            else:
                self.globalMemory.put(node.id, r2) 
