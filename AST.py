
class Node(object):

  def __init__(self, node_info):
      #if len(node_info) == 3:
      self.lineno = node_info['lno']
         #self.columnno = node_info['cno']
         #self.ptype = node_info['ptype']
    
  def accept(self, visitor, table = None):
      className = self.__class__.__name__
      # return visitor.visit_<className>(self)
      meth = getattr(visitor, 'visit_' + className, None)
      if meth!=None:
          return meth(self, table)

class ErrorNode(Node):
    pass

class Program(Node):
  def __init__(self, ext_decls, fundefs, instrs, pos):  
    self.ext_decls = ext_decls
    self.fundefs = fundefs
    self.instrs = instrs
    self.pos = pos
    
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
  def __init__(self, id, pos):
    self.id = id
    self.pos = pos

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

class FunctionDefList(Node):
  def __init__(self, fundefs):
    self.fundefs = fundefs

class FunctionDef(Node):
  def __init__(self, rettype, name, fmlparams, body, pos):
    self.rettype = rettype
    self.name = name
    self.fmlparams = fmlparams
    self.body = body
    self.pos = pos

class InstructionList(Node):
  def __init__(self, instrs):
    self.instrs = instrs

class PrintInstruction(Node):
  def __init__(self, expr):
    self.expr = expr

class ReturnInstruction(Node):
  def __init__(self, expr, pos):
    self.expr = expr
    self.pos = pos

class DeclarationList(Node):
  def __init__(self, decls):
    self.decls = decls

class Declaration(Node):
  def __init__(self, type, inits, pos):
    self.type = type
    self.inits = inits
    self.pos = pos

class InitList(Node):
  def __init__(self, inits):
    self.inits = inits

class Init(Node):
  def __init__(self, id, expr):
    self.id = id
    self.expr = expr

class ChoiceInstruction(Node):
  def __init__(self, cond, ithen, ielse = None):
    self.cond = cond
    self.ithen = ithen
    self.ielse = ielse

class WhileInstruction(Node):
  def __init__(self, kw, cond, instr):
    self.keyword = kw
    self.cond = cond
    self.instr = instr

class KeyWordInstruction(Node):
  def __init__(self, kw):
    self.keyword = kw 

class CompoundInstructions(Node):
  def __init__(self, decls, instrs):
    self.decls = decls
    self.instrs = instrs

class Assignment(Node):
  def __init__(self, id, expr):
    self.id = id
    self.expr = expr

class LabeledInstruction(Node):
  def __init__(self, kw, instr):
    self.keyword = kw
    self.instr = instr

class RepeatInstruction(Node):
  def __init__(self, kw_1, instrs, kw_2, cond ):
      self.kw_1 = kw_1
      self.kw_2 = kw_2
      self.instrs = instrs
      self.cond = cond

class ArgsList(Node):
  def __init__(self, args):
    self.args = args

class Arg(Node):
  def __init__(self, type, id):
    self.type = type
    self.id = id
