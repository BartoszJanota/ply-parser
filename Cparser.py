#!/usr/bin/python

from scanner import Scanner
from AST import *
import TreePrinter



class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')

    
    
    def p_program(self, p):
        """program : declarations fundefs instructions"""
        print p[1]
        print p[2]
        print p[3]
    
    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
                     
    
    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """


    def p_init(self, p):
        """init : ID '=' expression """


    
    def p_instructions(self, p):
        """instructions : instructions instruction"""
        p[0] = InstructionList(p[1].instrs + [ p[2] ])
    
    def p_instructions_single(self, p):
        """instructions : instruction """
        #print 'Captured instruction list with a single item = ', p[1]
        p[0] = InstructionList([ p[1] ])

    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr"""
        p[0] = p[1]
    
    
    def p_print_instr(self, p):
        """print_instr : PRINT expression ';' """
        #print 'Captured print instruction'
        p[0] = SimpleInstruction(p[1], p[2])

    #### TODO                   | PRINT error ';' """
    
    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
    
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
    
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

    
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
    
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
    
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """

    
    def p_condition(self, p):
        """condition : expression"""


    def p_const_integer(self, p):
        """const : INTEGER"""
        p[0] = Integer(p[1])

    def p_const_float(self, p):
        """const : FLOAT"""
        p[0] = Float(p[1])

    def p_const_string(self, p):
        """const : STRING"""
        p[0] = String(p[1])
    
    def p_expression_const(self, p):
        """expression : const"""
        p[0] = p[1]

    def p_expression_id(self, p):
        "expression : ID"
        p[0] = Variable(p[1])

    def p_expression_brackets(self, p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    #### TODO ????                  | '(' error ')'

    #### TODO ??? | ID '(' error ')' """

    def p_expression_fun_call(self, p):
        "expression : ID '(' expr_list_or_empty ')'"
        p[0] = FunctionCall(p[1], p[3])
    
    
    def p_expression_binary_op(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression"""

        p[0] = BinExpr(p[1], p[2], p[3])

    
    def p_expr_list_non_empty(self, p):
        """expr_list_or_empty : expr_list"""
        p[0] = p[1]

    def p_expr_list_empty(self, p):
        """expr_list_or_empty : """
        p[0] = ExprList([])
    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression"""
        p[0] = ExprList(p[1].exprs + [ p[3] ])
    
    def p_expr_list_single(self, p):
        """expr_list : expression"""   
        p[0] = ExprList([ p[1] ])
    
    
    def p_fundefs(self, p):
        """fundefs : fundef fundefs
                   |  """

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
    
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
    
    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
    
    def p_arg(self, p):
        """arg : TYPE ID """


    

