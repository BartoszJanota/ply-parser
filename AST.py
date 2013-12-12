
class Node(object):

    def __str__(self):
        return self.printTree()


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
    pass



class BinExpr(Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right
    print(left, op, right)

class ExprList(Node):
  def __init__(self, list, expr):
    self.list = list
    self.expr = expr

class FunctionCall(Node):
  def __init__(self, id, exprs):
    self.id = id
    self.exprs = exprs


