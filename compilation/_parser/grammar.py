from compilation._parser._parser import rule
from compilation._parser.ast_nodes import *

grammar = { 
    'PROGRAM': [
    rule('PROGRAM STML','program',lambda p: ProgramNode(p[1])),
    rule('PROGRAM ',None,lambda p: [])],
    'STML':[
    rule('STML STML STM',None,lambda p: StatementListNode(p[1].statements+[p[2]])),
    rule('STML ',None,lambda p: StatementListNode([]))],
    'STM':[
    rule('STM FUNDECL','stmt',lambda p: p[1]),
    rule('STM FUNCALL scolon','stmt',lambda p: p[1]),
    rule('STM RETURN','stmt',lambda p: p[1]),
    rule('STM ASSIGN scolon','stmt',lambda p: p[1]),
    rule('STM DECLARATION','stmt',lambda p: p[1]),
    rule('STM WHILE','stmt',lambda p: p[1]),
    rule('STM IF','stmt',lambda p: p[1]),
    rule('STM FLOW','stmt',lambda p: p[1]),
    rule('STM METHODCALL scolon','stmt',lambda p: p[1]),
    ],
    'ID':[
    rule('ID word','id',lambda p: p[1])],
    'FUNDECL':[
    rule('FUNDECL type ID OPTPARAM bl STML br','fundecl',lambda p: FunDeclNode(p[1],p[2],p[3],p[5]))],
    'OPTPARAM':[
    rule('OPTPARAM pl PARAMS pr','optparam',lambda p: p[2]),
    rule('OPTPARAM pl pr',None,lambda p: [])],
    'PARAMS':[
    rule('PARAMS PARAM comma PARAMS','param',lambda p: [p[1]]+p[3]),
    rule('PARAMS PARAM',None,lambda p: [p[1]])],
    'PARAM':[
    rule('PARAM type ID','param',lambda p:(p[1],p[2]))],
    'FUNCALL':[
    rule('FUNCALL ID OPTARG','funcall',lambda p: FunCallNode(p[1],p[2]))],
    'OPTARG':[
    rule('OPTARG pl ARGS pr','optarg',lambda p: p[2]),
    rule('OPTARG pl pr',None,lambda p: [])],
	'ARGS':[
    rule('ARGS EXP comma ARGS','args',lambda p: [p[1]]+p[3]),
    rule('ARGS EXP','arg',lambda p: [p[1]])],
    'RETURN':[
    rule('RETURN return EXP scolon','return',lambda p: ReturnNode(p[2]))],
    'DECLARATION':[
    rule('DECLARATION type ID assign EXP scolon','declaration',lambda p: DeclarationNode(p[1],p[2],p[4])),
    rule('DECLARATION type ID assign type OPTARG scolon','instance',lambda p: InstanceDeclarationNode(p[1],p[2],p[4],p[5]))],
    'ASSIGN':[
    rule('ASSIGN ID assign EXP','assign',lambda p: AssignNode(p[1],p[3]))],   
    'WHILE':[
    rule('WHILE while pl EXP pr bl STML br','while',lambda p: WhileNode(p[3],p[6]))],
    'IF':[
    rule('IF if pl EXP pr bl STML br','if',lambda p:IfElseNode(p[3],p[6],StatementListNode([]))),
    rule('IF if pl EXP pr bl STML br else bl STML br','if',lambda p:IfElseNode(p[3],p[6],p[10]))],
    'FLOW':[
    rule('FLOW continue scolon','continue',lambda p:ContinueNode()),
    rule('FLOW break scolon','break',lambda p: BreakNode())],
    'METHODCALL':[
    rule('METHODCALL ID dot ID OPTARG','method call',lambda p: MethodCallNode(p[1],p[3],p[4]))   
    ],
    'ATTR':[
    rule('ATTR ID dot ID','attr',lambda p: AttributeNode(p[1],p[3]))
    ],
    'LIST':[
    rule('LIST sbl ARGS sbr','list',lambda p: ListNode(p[2])),
    rule('LIST sbl sbr','list',lambda p: ListNode([]))],
    'LISTINDEX':[
    rule('LISTINDEX EXP sbl EXP sbr','listindex',lambda p: ListIndexNode(p[1],p[3]))],
    'EXP':[
    rule('EXP true','true',lambda p:  BooleanNode(p[1])),
    rule('EXP false','false',lambda p: BooleanNode(p[1])),
    rule('EXP int','int',lambda p: IntNode(p[1])),
    rule('EXP float','float',lambda p: FloatNode(p[1])),
    rule('EXP string','string',lambda p: StringNode(p[1])),
    rule('EXP ID',None,lambda p: VariableNode(p[1])),
    rule('EXP LIST',None,lambda p: p[1]),
    rule('EXP LISTINDEX',None,lambda p: p[1]),
    rule('EXP FUNCALL',None,lambda p: p[1]),
    rule('EXP METHODCALL',None,lambda p: p[1]),
    rule('EXP ATTR',None,lambda p: p[1]),
    rule('EXP pl ARITHEXP pr','arith',lambda p: p[2]),
    rule('EXP ARITHEXP','arith',lambda p: p[1])],
    'ARITHEXP':[
    rule('ARITHEXP ARITHEXP add TERM','add',lambda p: PlusNode(p[1],p[2],p[3])),
    rule('ARITHEXP ARITHEXP minus TERM','minus',lambda p: MinusNode(p[1],p[2],p[3])),
    rule('ARITHEXP TERM',None,lambda p: p[1])],
    'TERM':[
    rule('TERM TERM mult EXP','mult',lambda p: MultNode(p[1],p[2],p[3])),
    rule('TERM TERM div EXP','div',lambda p: DivNode(p[1],p[2],p[3])),
    rule('TERM CONDEXP',None,lambda p: p[1])],
    'CONDEXP':[
    rule('CONDEXP EXP',None,lambda p: p[1]),
    rule('CONDEXP not CONDEXP','not',lambda p: NotNode(p[2])),
    rule('CONDEXP EXP and CONDEXP','and',lambda p: AndNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP or CONDEXP','or',lambda p: OrNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP greatequal EXP','greatequal',lambda p: GreatEqualNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP lessequal EXP','lessequal',lambda p: LessEqualNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP great EXP','great',lambda p: GreatNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP less EXP','less',lambda p: LessNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP equal EXP','equal',lambda p: EqualNode(p[1],p[2],p[3])),
    rule('CONDEXP EXP notequal EXP','notequal',lambda p: NotEqualNode(p[1],p[2],p[3])),
    ]
}