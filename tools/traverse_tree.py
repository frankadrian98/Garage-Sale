from _parser.ast_nodes import *
from tools import visitor

class Returns:

    def __init__(self):
        self.returns = []

    @visitor.on('node')
    def visit(self,node):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node):
        self.visit(node.stml)

    @visitor.when(StatementListNode)
    def visit(self,node):
        for stmt in node.statements:
            self.visit(stmt)

    @visitor.when(FunDeclNode)
    def visit(self,node):
        pass
    
    @visitor.when(FunCallNode)
    def visit(self,node):
        pass

    @visitor.when(ReturnNode)
    def visit(self,node): 
        self.returns.append(node)
        
    @visitor.when(WhileNode)
    def visit(self,node): 
        self.visit(node.whileblock)
    
    @visitor.when(IfElseNode)
    def visit(self,node): 
        self.visit(node.ifblock)
        if len(node.elseblock.statements)>0:
            self.visit(node.elseblock)


class PrintAST:
    def __init__(self):
        self.ast = []
        
        self.tab_style = ' '*2

    @visitor.on('node')
    def visit(self,node,tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node):
        self.visit(node.stml)

    @visitor.when(StatementListNode)
    def visit(self,node):
        for stmt in node.statements:
            self.ast.append(self.tab_style*tabs +  'Statement')
            self.visit(stmt)

    @visitor.when(FunDeclNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'FunDecl')
        self.visit(node.args)
        self.visit(node.body)
    
    @visitor.when(FunCallNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'FunCall')
        self.visit(node.args)

    @visitor.when(ReturnNode)
    def visit(self,node): 
        self.ast.append(self.tab_style*tabs +'Return')
        self.visit(node.exp)
        

    @visitor.when(AssignNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Assign')
        self.visit(node.exp)
        

    @visitor.when(DeclarationNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Declare') 
        self.visit(node.exp)

    @visitor.when(WhileNode)
    def visit(self,node): 
        self.ast.append(self.tab_style*tabs +'While')
        self.visit(node.cond)
        self.visit(node.whileblock)
    
    @visitor.when(IfElseNode)
    def visit(self,node): 
        self.ast.append(self.tab_style*tabs +  'if ')
        self.visit(node.cond)
        self.visit(node.ifblock)
        if len(node.elseblock.statements)>0:
            self.ast.append(self.tab_style*tabs +  'else:')
            self.visit(node.elseblock)

    @visitor.when(FlowNode)
    def visit(self,node):
        if type(node) is ContinueNode:
            self.ast.append(self.tab_style*tabs +'Flow')
        if type(node) is BreakNode:
            self.ast.append(self.tab_style*tabs +'Break')
    
    @visitor.when(ListNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'List')
        for exp in node.content:
            self.visit(exp)


    @visitor.when(ListIndexNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'ListIndexNode')
        self.visit(node.exp)
        self.visit(node.index,tabs+2)

    @visitor.when(LiteralNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Literal')

    @visitor.when(VariableNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Variable')

    @visitor.when(NotNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Not')
        self.visit(node.cond)

    @visitor.when(BinaryNode)
    def visit(self,node):
        self.ast.append(self.tab_style*tabs +'Binary')
        self.visit(node.left)
        self.visit(node.right)

