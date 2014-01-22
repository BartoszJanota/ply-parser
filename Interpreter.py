
import AST
import SymbolTable
#from Memory import *
from Exceptions import  *
from visit import *


class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...


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
        print 'Visited a Program'
        
