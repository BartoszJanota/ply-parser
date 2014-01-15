#!/usr/bin/python



class TypeChecker(object):

    def visit_BinExpr(self, node):
        type1 = node.left.accept(self)
        type2 = node.right.accept(self)
        op    = node.op;
        # ... 
        #
 
    def visit_RelExpr(self, node):
        type1 = node.left.accept(self);
        type2 = node.right.accept(self);
        # ... 
        #

    def visit_Integer(self, node):
        return 'int'

    #def visit_Float(self, node):
    # ... 
    # 

    # ... 
    # 


