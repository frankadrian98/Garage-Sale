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

default_path = os.getcwd()+ '/example_templates/'
default_file = 'fake_simulation.gar'


def main():

    with open(default_path +default_file  ,'r') as f:
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
    errors = main()
    if not errors:
        exec(open(default_path+'/transpiled_'+default_file[:-4]+'.py').read())
    