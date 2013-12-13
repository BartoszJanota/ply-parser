
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self):
        pass
        # TODO

    @addToClass(AST.Const)
    def printTree(self):
        return str(self.value)

    @addToClass(AST.ExprList)
    def printTree(self):
      return ', '.join(str(expr) for expr in self.exprs)

    @addToClass(AST.FunctionCall)
    def printTree(self):
      #print 'Function call', self.params
      return 'FUNCALL ' + str(self.params)

    @addToClass(AST.InstructionList)
    def printTree(self):
      return '\n'.join(str(instr) for instr in self.instrs)

    @addToClass(AST.SimpleInstruction)
    def printTree(self):
      return self.keyword + ' ' + str(self.expr)


