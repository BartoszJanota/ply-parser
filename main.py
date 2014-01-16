
import sys
import logging
import logging.handlers
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from AST import *


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    text = file.read()
    #parser.parse(text, lexer=Cparser.scanner, debug=logger)
    parser.parse(text, lexer=Cparser.scanner)
    ast = parser.parse(text, lexer=Cparser.scanner)
    ast.accept(TypeChecker())

