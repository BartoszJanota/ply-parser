
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):

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
        r1 = node.left.iaccept(self)[0]
        r2 = node.right.iaccept(self)[0]

        return self.actions[node.op](r1, r2)


    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.WhileInstruction)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r


    @when(AST.Program)
    def visit(self, node):
        node.ext_decls.iaccept(self)
        node.fundefs.iaccept(self)
        node.instrs.iaccept(self)
    
    @when(AST.InstructionList)
    def visit(self, node):
        for instr in node.instrs:
            instr.iaccept(self)

    @when(AST.PrintInstruction)
    def visit(self, node):
        print node.expr.iaccept(self)

    @when(AST.Variable)
    def visit(self, node):
        localVar = self.functionMemory.get(node.id)
        if localVar:
            return localVar
        else:
            return self.globalMemory.get(node.id)

    @when(AST.DeclarationList)
    def visit(self, node):
        for decl in node.decls:
            decl.iaccept(self)

    @when(AST.Declaration)
    def visit(self, node): 
        node.inits.iaccept(self)

    @when(AST.InitList)
    def visit(self, node):
        for init in node.inits:
            init.iaccept(self)

    @when(AST.Init)
    def visit(self, node):
        val = node.expr.iaccept(self)
        self.globalMemory.put(node.id, val)

