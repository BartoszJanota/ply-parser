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

    def handle_error(self, where, p):
        print("Syntax error in %s at line %d, column %d, at token LexToken(%s, '%s')" %\
          (where, p.lineno, self.scanner.find_tok_column(p), p.type, p.value))

    def p_error(self, p):
        if not p:
            print 'Unexpected end of input'
        else:
            # let the productions handle the error on their own
            pass
    
    
    def p_program(self, p):
        """program : ext_declarations fundefs instructions"""
        p[1].draw()  
        p[2].draw()
        p[3].draw() 
    
    def p_ext_declarations(self,p):
        """ext_declarations : declarations"""
        p[0] = p[1]

    def p_declarations(self, p):
        """declarations : declarations declaration"""
        if p[2]:            
            p[0] = DeclarationList(p[1].decls + [ p[2] ])
        else: # error
            p[0] = p[1]
    
    def p_declarations_single(self, p):
        """declarations : declaration"""
        if p[1]:
            p[0] = DeclarationList([ p[1] ])
        else: # error
            p[0] = DeclarationList([ ])                 

    def p_declaration_blank(self, p):
        """declarations : """
        p[0] = DeclarationList([ ])                 
    
    def p_declaration(self, p):
        """declaration : TYPE inits ';' """
        p[0] = Declaration(p[1], p[2])
                       
    def p_declaration_error(self, p):
        """declaration : error ';' """
        self.handle_error('declaration', p[1])

    def p_inits(self, p):
        """inits : inits ',' init"""
        p[0] = InitList(p[1].inits + [ p[3] ])

    def p_inits_single(self, p):
        """inits : init"""
        p[0] = InitList([ p[1] ])

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = Init(p[1], p[3])
    
    def p_instructions(self, p):
        """instructions : instructions instruction"""
        if p[2]:
          p[0] = InstructionList(p[1].instrs + [ p[2] ])
        else:
          p[0] = p[1]
    
    def p_instructions_single(self, p):
        """instructions : instruction """
        if p[1]:
          p[0] = InstructionList([ p[1] ])
        else:
          p[0] = InstructionList([ ])

    #def p_instruction_brackets(self,p):
    #    """instruction : '{' instruction '}'"""
    #    p[0] = p[2]

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
        p[0] = SimpleInstruction(p[1], p[2])

    def p_print_error(self, p):
        """print_instr : PRINT error ';' """
        self.handle_error('print instruction', p[2])
    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = LabeledInstruction(p[1], p[3])
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        if p[3]:
            p[0] = Assignment(p[1], p[3])
        else: # error
            pass
    
    def p_assignment_error(self, p):
        """assignment : ID '=' error ';' """
        self.handle_error('assignment', p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

    
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction"""
        p[0] = WhileInstruction(p[1], p[3], p[5])

    def p_while_error(self, p):
        """while_instr : WHILE '(' error ')' instruction """        
        self.handle_error('while instruction', p[3])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
    
    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = SimpleInstruction(p[1], p[2])
    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = KeyWordInstruction(p[1])

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = KeyWordInstruction(p[1])    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions '}' """
        p[0] = CompoundInstructions(p[2], p[3])

    
    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


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

    def p_expression_brackets_error(self, p):
        "expression : '(' error ')'"
        self.handle_error("expression (bracket)", p[2])

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
        """fundefs : fundefs fundef"""
        p[0] = FunctionDefList(p[1].fundefs + [ p[2] ])

    def p_fundefs_empty(self, p):
        """fundefs : """
        p[0] = FunctionDefList([])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        ## TODO: use FunctionDef class
    
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
    
    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
    
    def p_arg(self, p):
        """arg : TYPE ID """


    

