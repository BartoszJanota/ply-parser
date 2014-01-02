
class Node(object):
  def draw(self):
      self.printTree(0)


class Const(Node):
  def __init__(self, value):
    self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
  def __init__(self, id):
    self.id = id



class BinExpr(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right
    #sprint(left, op, right)

class ExprList(Node):
  def __init__(self, exprs):
    self.exprs = exprs

class FunctionCall(Node):
  def __init__(self, id, params):
    self.id = id
    self.params = params

class InstructionList(Node):
  def __init__(self, instrs):
    self.instrs = instrs

class SimpleInstruction(Node):
  def __init__(self, kw, expr):
    self.keyword = kw
    self.expr = expr

class DeclarationList(Node):
  def __init__(self, decls):
    self.decls = decls

class Declaration(Node):
  def __init__(self, type, inits):
    self.type = type
    self.inits = inits

class InitList(Node):
  def __init__(self, inits):
    self.inits = inits

class Init(Node):
  def __init__(self, id, expr):
    self.id = id
    self.expr = expr 
