from compilation.tools import visitor
from compilation._parser.ast_nodes import *

class Transpiler:
    def __init__(self):
        self.code = []
        self.tab_style = ' '*4
        self.code.append('from simulation.simulation import *')
        self.code.append('from simulation.customer import *')
        self.code.append('from compilation.language.built_ins import *')
        self.code.append('from simulation.Genetic_algorithm import MakeSim')


    @visitor.on('node')
    def visit(self,node,tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node,tabs = 0):
        self.visit(node.stml)

    @visitor.when(StatementListNode)
    def visit(self,node,tabs = 0):
        for stmt in node.statements:
            handled_stmt = self.visit(stmt,tabs)
            if handled_stmt:
                self.code.append(self.tab_style*tabs + handled_stmt)

    @visitor.when(FunDeclNode)
    def visit(self,node,tabs = 0):
        self.code.append(self.tab_style*tabs+'def '+node.id + '(' + ', '.join(node.args)+'):')
        self.visit(node.body,tabs+1)
    
    @visitor.when(FunCallNode)
    def visit(self,node,tabs = 0):
        return(node.id + '(' + ', '.join([self.visit(a,tabs) for a in node.args])+')')

    @visitor.when(ReturnNode)
    def visit(self,node,tabs = 0): 
        return('return '+self.visit(node.exp,tabs))
        

    @visitor.when(AssignNode)
    def visit(self,node,tabs = 0):
        return(node.id+ ' = '+self.visit(node.exp,tabs))
        

    @visitor.when(DeclarationNode)
    def visit(self,node,tabs = 0): 
        declaration = self.visit(node.exp,tabs)
        return(node.id+ ' = '+ declaration)

    @visitor.when(InstanceDeclarationNode)
    def visit(self,node,tabs = 0):
        return (node.id + ' = ' + node.class_type+'(' + ', '.join([self.visit(a,tabs) for a in node.args])+')')

    @visitor.when(WhileNode)
    def visit(self,node,tabs = 0): 
        self.code.append(self.tab_style*tabs + 'while '+self.visit(node.cond,tabs)+':')
        self.visit(node.whileblock,tabs+1)
    
    @visitor.when(IfElseNode)
    def visit(self,node,tabs = 0): 
        self.code.append(self.tab_style*tabs + 'if '+self.visit(node.cond,tabs)+':')
        self.visit(node.ifblock,tabs+1)
        if len(node.elseblock.statements)>0:
            self.code.append(self.tab_style*tabs + 'else:')
            self.visit(node.elseblock,tabs+1)

    @visitor.when(FlowNode)
    def visit(self,node,tabs = 0):
        if type(node) is ContinueNode:
            return 'continue' 
        if type(node) is BreakNode:
            return 'break'
    
    @visitor.when(ListNode)
    def visit(self,node,tabs = 0):
        new_content = []
        for exp in node.content:
            new_content.append(self.visit(exp))
        return '[' + ', '.join(new_content) + ']'

    @visitor.when(ListIndexNode)
    def visit(self,node,tabs = 0):
        return self.visit(node.exp,tabs)+'['+self.visit(node.index,tabs)+']'

    @visitor.when(LiteralNode)
    def visit(self,node,tabs = 0):
        return str(node.value)

    @visitor.when(VariableNode)
    def visit(self,node,tabs = 0):
        return str(node.id)

    @visitor.when(NotNode)
    def visit(self,node,tabs = 0):
        return 'not '+self.visit(node.cond,tabs)

    @visitor.when(BinaryNode)
    def visit(self,node,tabs = 0):
        left = self.visit(node.left,tabs)
        right = self.visit(node.right,tabs)
        if type(node) is PlusNode:
            return '('+ left + ' + '+ right + ')'
        if type(node) is MinusNode:
            return '('+ left + ' - '+ right + ')'
        if type(node) is MultNode:
            return '('+ left + ' * '+ right + ')'
        if type(node) is DivNode:
            return '('+ left + ' + '+ right + ')'
        if type(node) is AndNode:
            return '('+ left + ' and '+ right + ')'
        if type(node) is OrNode:
            return '('+ left + ' or '+ right + ')'
        if type(node) is GreatEqualNode:
            return '('+ left + ' >= '+ right + ')'
        if type(node) is LessEqualNode:
            return '('+ left + ' <= '+ right + ')'
        if type(node) is GreatNode:
            return '('+ left + ' > '+ right + ')'
        if type(node) is LessNode:
            return '( '+ left + ' < '+ right + ' )'
        if type(node) is EqualNode:
            return '( '+ left + ' == '+ right + ' )'
        if type(node) is NotEqualNode:
            return '( '+ left + ' != '+ right + ' )'

    
    @visitor.when(AttributeNode)
    def visit(self,node,tabs = 0):
        return (node.class_id + '.' + node.id)

    @visitor.when(MethodCallNode)
    def visit(self,node,tabs = 0):
        return(node.class_id +'.'+node.method_id + '(' + ', '.join([self.visit(a,tabs) for a in node.method_args])+')')
