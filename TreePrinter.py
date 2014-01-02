
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def tprint(l, s):
  print "| " * l + s

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, l):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    @addToClass(AST.BinExpr)
    def printTree(self, l):
      tprint(l, self.op)
      self.left.printTree(l+1)
      self.right.printTree(l+1)

    @addToClass(AST.Const)
    def printTree(self, l):
        tprint(l, self.value)

    @addToClass(AST.ExprList)
    def printTree(self, l):
      for expr in self.exprs:
        expr.printTree(l)

    @addToClass(AST.FunctionCall)
    def printTree(self, l):
      #print 'Function call', self.params
      tprint(l, 'FUNCALL ')
      tprint(l+1, self.id)
      self.params.printTree(l+1)

    @addToClass(AST.InstructionList)
    def printTree(self, l):
      for instr in self.instrs:
        instr.printTree(l)

    @addToClass(AST.SimpleInstruction)
    def printTree(self, l):
      tprint(l, self.keyword.upper())
      self.expr.printTree(l+1)

    @addToClass(AST.Variable)
    def printTree(self, l):
      tprint(l, self.id)

    @addToClass(AST.DeclarationList)
    def printTree(self, l):
      for decl in self.decls:
        decl.printTree(l)

    @addToClass(AST.Declaration)
    def printTree(self, l):
      tprint(l, 'DECL')
      tprint(l+1, self.type)
      self.inits.printTree(l+1)

    @addToClass(AST.FunctionDefList)
    def printTree(self, l):
      for fundef in self.fundefs:
        fundef.printTree(l)

    @addToClass(AST.InitList)
    def printTree(self, l):
      for init in self.inits:
        init.printTree(l+1)

    @addToClass(AST.Init)
    def printTree(self, l):
      tprint(l, '=')
      tprint(l+1, self.id)
      self.expr.printTree(l+1)

