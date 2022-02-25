
from tools import visitor
from _parser.ast_nodes import ProgramNode,FunDeclNode,DeclarationNode,StatementListNode,InstanceDeclarationNode

class TypeBuilder:

    def __init__(self,typecontext):
        self.typecontext = typecontext
        self.current_type = None
        self.errors = []
    
    @visitor.on('node')
    def visit(self,node):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node):
        self.current_type = self.typecontext.get_type('Main')
        self.visit(node.stml)

    @visitor.when(StatementListNode)
    def visit(self,node):
        for stmt in node.statements:
            self.visit(stmt)

    @visitor.when(FunDeclNode)
    def visit(self,node):    
        
        try:
            return_type = self.typecontext.get_type(node.type)
        except Exception as e:
            self.errors.append(e.args[0])

        same_len = True        
        arg_types = []

        for _type in node.arg_types:
            try:
                arg_type = self.typecontext.get_type(_type)
                arg_types.append(arg_type)
            except Exception as e:
                same_len = False
                self.errors.append(e.args[0])
        if same_len:
            try:
                self.current_type.define_method(node.id, return_type, node.args, arg_types)
            except Exception as e:
                self.errors.append(e.args[0])



    @visitor.when(DeclarationNode)
    def visit(self,node):
        try:
            _type = self.typecontext.get_type(node.type)
            self.current_type.define_attribute(node.id, _type)
        except Exception as e:
            self.errors.append(e.args[0])

    @visitor.when(InstanceDeclarationNode)
    def visit(self,node):
        try:
            _type = self.typecontext.get_type(node.type)
            self.current_type.define_attribute(node.id, _type)
        except Exception as e:
            self.errors.append(e.args[0])
