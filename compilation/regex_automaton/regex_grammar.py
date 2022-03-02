
from compilation._parser._parser import rule
from compilation.regex_automaton.regex_ast import *

test_grammar = {

    'O':[
    rule('O O or C',None,lambda p: UnionNode(p[1],p[3])),
    rule('O C',None,lambda p: p[1]),
    rule('O ',None,lambda p: EpsilonNode())
    ],
    'C':[
    rule('C C Q',None,lambda p: ConcatNode(p[1],p[2])),
    rule('C Q',None,lambda p: p[1])
    ],
    'Q':[
    rule('Q A star',None,lambda p: StarNode(p[1])),
    rule('Q A plus',None,lambda p: PlusNode(p[1])),
    rule('Q A question',None,lambda p: QuestionNode(p[1])),
    rule('Q A',None,lambda p: p[1])
    ],
    'A':[
    rule('A element',None,lambda p: ElementNode(p[1])),
    rule('A pl O pr',None,lambda p: p[2]),
    rule('A sbl B sbr',None,lambda p: p[2]),
    rule('A O',None,lambda p: p[1]),
    ],
    'B':[
    rule('B not I',None,lambda p: ComplementNode(p[2])),    
    rule('B I',None,lambda p: BracketNode(p[1])),   
    ],
    'I':[
    rule('I I T',None,lambda p: MultiElemBracketNode(p[1],p[2])),
    rule('I T',None,lambda p: p[1])
    ],
    'T':[
    rule('T T minus S',None,lambda p: RangeNode(p[1],p[3])),
    rule('T S',None,lambda p: p[1])    
    ],
    'S':[
    rule('S element',None, lambda p: InnerBracketNode(p[1]))   
    ]
}