from compilation._parser._parser import parse
from compilation._parser.grammar import grammar
from compilation._lexer.token_matcher import token_matcher
from compilation._lexer._lexer import tokenize
from compilation.transpiler.transpiler import Transpiler
from compilation.semantics.type_collector import TypeCollector
from compilation.semantics.type_builder import TypeBuilder
from compilation.semantics.type_checker import TypeChecker
from compilation.semantics.context import TypeContext
from compilation.tools.print_colors import Color
import os
import sys
from pathlib import Path

default_path = os.getcwd()+ '/example_templates/'
default_file = 'program.gar'

def change_path(pth):
    p = pth.strip('\\')
    new_p= ""
    for i in range(len(p)-1):
        new_p+= p[i] + '/'
    default_path = new_p
    default_file = p[-1]

def main(pth = None):
    _f = default_path +default_file 
    if pth:
        _f = Path(pth)
        change_path(pth)
    with open(_f  ,'r') as f:
        code = f.read()
    tokens = tokenize(code, tuple(token_matcher))
    parsed =  parse(grammar, {}, tokens, grammar['PROGRAM'][0])
    tcollector = TypeCollector(TypeContext())
    tcollector.visit(parsed)
    tbuilder = TypeBuilder(tcollector.typecontext)
    tbuilder.visit(parsed)
    tchecker = TypeChecker(tbuilder.typecontext,tbuilder.errors)
    tchecker.visit(parsed)
    trans = Transpiler()
    
    trans.visit(parsed)
    
    for err in tchecker.errors:
        print(Color.FAIL+err+Color.ENDC)
    for err in tchecker.warnings:
        print(Color.WARNING+err+Color.ENDC)


    transpiled_code = '\n'.join([str(line) for line in trans.code])
    if len(tchecker.errors) == 0:
        f = open(default_path+'/transpiled_'+default_file[:-4]+'.py',"w+")
        f.write(transpiled_code)
        f.close()
    return tchecker.errors
    
if __name__ == "__main__":
    if len(sys.argv)>1:       
        pth  = sys.argv[1]
        print(pth)
        if Path(pth).is_file() and pth.endswith('.gar'):
            errors = main(pth)
        else:
            print(Color.FAIL+'File must exist and be of type gar'+Color.ENDC)
            exit(0)
    else:
        errors = main()
    
    if not errors:
        exec(open(default_path+'/transpiled_'+default_file[:-4]+'.py').read())
    