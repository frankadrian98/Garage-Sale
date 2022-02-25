from _parser._parser import parse
from _parser.grammar import grammar
from _lexer.token_matcher import token_matcher
from _lexer._lexer import tokenize
from transpiler.transpiler import Transpiler
from semantics.type_collector import TypeCollector
from semantics.type_builder import TypeBuilder
from semantics.type_checker import TypeChecker
from semantics.context import TypeContext
from tools.print_colors import Color
import os

default_path = os.getcwd()+ '/example_templates/'
default_file = 'test_scopes.gar'


def main():

    

    with open(default_path +default_file  ,'r') as f:
        code = f.read()

    test =  parse(grammar, {}, tokenize(code, token_matcher), grammar['PROGRAM'][0])


    tcollector = TypeCollector(TypeContext())
    tcollector.visit(test)
    tbuilder = TypeBuilder(tcollector.typecontext)
    tbuilder.visit(test)
    tchecker = TypeChecker(tbuilder.typecontext,tbuilder.errors)
    tchecker.visit(test)
    trans = Transpiler()

    trans.visit(test)
    for err in tchecker.errors:
        print(Color.FAIL+err+Color.ENDC)
    for err in tchecker.warnings:
        print(Color.WARNING+err+Color.ENDC)


    transpiled_code = '\n'.join([str(line) for line in trans.code])
    if len(tchecker.errors) == 0:
        f = open(default_path+'/transpiled_'+default_file[:-4]+'.py',"w+")
        f.write(transpiled_code)
        f.close()
    
    
if __name__ == "__main__":
    main()
    exec(open(default_path+'/transpiled_'+default_file[:-4]+'.py').read())