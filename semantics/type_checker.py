
from _parser.ast_nodes import *
from semantics.context import TypeContext,Context
from tools import visitor,traverse_tree
from language.types import *


class TypeChecker:

    def __init__(self,typecontext,errors):
        self.typecontext = typecontext
        self.errors = errors
        self.warnings = []
        self.current_type = None
        self.in_while = False

    @visitor.on('node')
    def visit(self,node,context):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node,context =None):
        self.current_type = self.typecontext.get_type('Main')
        context = Context()
        self.visit(node.stml,context)

    @visitor.when(StatementListNode)
    def visit(self,node,context):
        for stmt in node.statements:
            self.visit(stmt,context)

    @visitor.when(FunDeclNode)
    def visit(self,node,context):

        
        inner_context = context.create_child_context()

        try:
            return_type = self.typecontext.get_type(node.type)
        except Exception as e:
            self.errors.append(e.args[0])

        same_len = True
        arg_types = []

        for i in range(len(node.arg_types)):
            try:
                arg_type = self.typecontext.get_type(node.arg_types[i])
                arg_types.append(arg_type)
                
            except Exception as e:
                same_len = False
                self.errors.append(e.args[0])
            try:
                inner_context.define_local_var(node.args[i],arg_type)
            except Exception as e:
                self.errors.append(e.args[0])
        if same_len:
            if not context.define_fun(node.id, return_type, node.args, arg_types):
                self.errors.append('There is already a function named '+node.id + '() with '+ str(len(node.args))+' args') 

        self.visit(node.body, inner_context)
        void = return_type.name == VoidType().name
        ret = traverse_tree.Returns()
        ret.visit(node.body)
        if len(ret.returns)>0:
            if void:
                self.errors.append('The type of ' + node.id+'() is void but a return call was found')
            for stmt in ret.returns:
                infered_type = stmt.exp.computed_type
                if not infered_type :
                    self.errors.append('Could not infered the type of the function'+node.id)
                elif return_type != infered_type:
                    self.warnings.append('There is a branch of ' +node.id+'() funtion with '+infered_type.name + ' as infered type while it\'s return type is '+return_type.name)
        elif not void:
            self.errors.append('Expected '+return_type.name+ ' return type for funcion'+node.id+'(), but no return call was found')

    @visitor.when(FunCallNode)
    def visit(self,node,context):
        funcall_types = []
        for elem in node.args:
            self.visit(elem,context)
            funcall_types.append(elem.computed_type)
        try:
            called_fun = context.get_fun(node.id,len(node.args))
            node.computed_type = called_fun.return_type
            formal_funcall = Method(node.id,node.computed_type,node.args,funcall_types)
            if not formal_funcall == called_fun:
                node.computed_type = UnknownType()
                self.errors.append('Wrong parameters entry for function '+node.id+'()')
        except Exception as e:
            try:
                class_method = self.current_type.get_method(node.id,len(node.args))
                formal_funcall = Method(node.id,class_method.return_type,node.args,funcall_types)
                if not formal_funcall == class_method:
                    node.computed_type = UnknownType()
                    self.errors.append('Wrong parameters entry for function '+node.id+'()')
                else:
                    node.computed_type = class_method.return_type
            except Exception as er:
                self.errors.append(e.args[0])
                unknown_type = UnknownType()
                node.computed_type = unknown_type
                context.define_fun(node.id,unknown_type,node.args,[unknown_type for i in node.args])


    @visitor.when(ReturnNode)
    def visit(self,node,context):
        self.visit(node.exp,context)
        node.computed_type = node.exp.computed_type
    
    @visitor.when(AssignNode)
    def visit(self,node,context):
        try:
            var = context.get(node.id)
            self.visit(node.exp,context)
            if var.type != node.exp.computed_type:
                self.errors.append('Cannot assign '+ node.exp.computed_type.name+' to '+var.type.name)
        except Exception as e:
            self.errors.append(e.args[0])

    @visitor.when(DeclarationNode)
    def visit(self,node,context):
        try:
            _type = self.typecontext.get_type(node.type)
        except Exception as e:
            self.errors.append(e.args[0])
            _type = UnknownType()

        if not context.define_var(node.id,_type): 
            self.errors.append('There is already a variable with '+node.id+' as id')

        self.visit(node.exp,context)

        if _type != node.exp.computed_type:
            if not node.exp.computed_type:
                node.exp.computed_type = UnknownType()
            self.errors.append('Cannot declare '+ node.exp.computed_type.name+' as '+ _type.name)
        else:
            _type.content_type = node.exp.computed_type.content_type if node.exp.computed_type else UnknownType()

    @visitor.when(InstanceDeclarationNode)
    def visit(self,node,context):
        try:
            _type = self.typecontext.get_type(node.type)
        except Exception as e:
            self.errors.append(e.args[0])
            _type = UnknownType()

        if not context.define_var(node.id,_type): 
            self.errors.append('There is already a variable with '+node.id+' as id')
        
        
        try:
            class_type = self.typecontext.get_type(node.class_type)
        except Exception as e:
            self.errors.append(e.args[0])
            class_type = UnknownType()

        if _type != class_type:
            self.errors.append('Cannot declare '+ class_type.name+' as '+ _type.name)
            node.computed_type = UnknownType()
        else:
            intstance_param_types = []
            for elem in node.args:
                self.visit(elem,context)
                intstance_param_types.append(elem.computed_type)
            instance_method = Method(node.class_type,class_type,[x for x in range(len(node.args))],intstance_param_types)
            try:
                saved_method = self.current_type.get_method(node.class_type,len(node.args))
                if saved_method == instance_method:
                    node.computed_type = class_type
                else:
                    self.errors.appen('Found')
                    node.computed_type = UnknownType()
            except Exception as e:
                self.errors.append(e.args[0])
                node.computed_type = UnknownType()
        

    @visitor.when(WhileNode)
    def visit(self,node,context):

        self.visit(node.cond,context)
        if node.cond.computed_type.name != 'bool':
            self.errors.append('While condition must be bool type, found '+node.cond.computed_type.name)
        self.in_while = True
        self.visit(node.whileblock,context)
        self.in_while = False

    @visitor.when(IfElseNode)
    def visit(self,node,context):
        self.visit(node.cond,context)
        if node.cond.computed_type.name != 'bool':
            self.errors.append('If condition must be bool type, found '+node.cond.computed_type.name)
        self.visit(node.ifblock,context)
        self.visit(node.elseblock,context)

    @visitor.when(FlowNode)
    def visit(self,node,context):
        if type(node) is ContinueNode and not self.in_while:
            self.errors.append('Continue call must be in while block')
        if type(node) is BreakNode and not self.in_while:
            self.errors.append('Break call must be in while block')
            
    @visitor.when(ListNode)
    def visit(self,node,context):
        node.computed_type = ListType()
        content_types = []
        for elem in node.content:
            self.visit(elem,context)
            content_types.append(elem.computed_type.name)
        type_count = len(set(content_types))
        if type_count > 1:
            self.errors.append('Expected only one type for list elements, found '+str(type_count))
            return
        if content_types:
            try:
                node.computed_type.content_type = self.typecontext.get_type(content_types[0])
            except Exception as e:
                self.errors.append(e.args[0])
                node.computed_type = UnknownType()


    @visitor.when(ListIndexNode)
    def visit(self,node,context):
        self.visit(node.exp,context)
        exp_type = node.exp.computed_type
        if exp_type.name != 'list':
            self.errors.append('Expected list as source type, found '+exp_type.name)
            node.computed_type = UnknownType()
        else:
            self.visit(node.index,context)
            index_type = node.index.computed_type
            if index_type.name != 'int':
                self.errors.append('Expected int as index type, found '+index_type.name)
                node.computed_type = UnknownType()
            else:
                try:
                    node.computed_type = exp_type.content_type
                except Exception as e:
                    self.errors.append(e.args[0])
                    node.computed_type = UnknownType()


    @visitor.when(VariableNode)
    def visit(self,node,context):
        try:
            var = context.get(node.id)
            node.computed_type = var.type
        except Exception as e:
            self.errors.append(e.args[0])
            node.computed_type = UnknownType()

    @visitor.when(LiteralNode)
    def visit(self,node,context):
        try:
            node.computed_type = self.typecontext.get_type(node.type)
        except Exception as e:
            self.errors.append(e.args[0])
            node.computed_type = UnknownType()

    @visitor.when(NotNode)
    def visit(self,node,context):
        self.visit(node.cond,context)
        not_cond_type = node.cond.computed_type
        if not_cond_type.name != 'bool':
            node.computed_type = UnknownType()
            self.errors.append('Not Call expected bool expression, found'+not_cond_type.name)
        else:
            node.computed_type = not_cond_type

        
    @visitor.when(BinaryNode)
    def visit(self,node,context):
        self.visit(node.left,context)
        self.visit(node.right,context)
        left_type = node.left.computed_type
        right_type = node.right.computed_type
        if type(node) is PlusNode or type(node) is MinusNode or type(node) is MultNode or type(node) is DivNode:
            if left_type.name == 'int' and (right_type.name == 'int' or right_type.name == 'float') :
                if right_type.name == 'int':
                    node.computed_type = left_type
                else:
                    node.computed_type = right_type
            elif left_type.name == 'float' and (right_type.name == 'int' or right_type.name == 'float'):
                node.computed_type = left_type
            else:
                node.computed_type = UnknownType()
                self.errors.append('The operation '+node.operator + ' is not defined between types '+ left_type.name + ' and '+right_type.name)
        elif type(node) is AndNode or type(node) is OrNode:
            if left_type.name != 'bool' or right_type.name != 'bool':
                self.errors.append('The operation '+node.operator + 'is not defined for types '+left_type.name + ' and '+right_type.name)
            else:
                node.computed_type = BooleanType()
        elif type(node) is GreatEqualNode or type(node) is LessEqualNode or type(node) is GreatNode or type(node) is LessNode:
            if left_type != right_type or (left_type.name != 'int' and left_type.name != 'float'):
                node.computed_type = UnknownType()
                self.errors.append('The operation '+node.operator + 'is not defined for types '+left_type.name + ' and '+right_type.name)
            else:
                node.computed_type = BooleanType()
        elif type(node) is EqualNode or type(node) is NotEqualNode:
            node.computed_type = BooleanType()

    @visitor.when(AttributeNode)
    def visit(self,node,context):
        try:
            class_type = context.get(node.class_id).type
            class_attr = class_type.get_attribute(node.id)
            node.computed_type = class_attr.type
        except Exception as e:
            self.errors.append(e.args[0])
        

    @visitor.when(MethodCallNode)
    def visit(self,node,context):
        try:
            class_type = context.get(node.class_id).type
            class_method = class_type.get_method(node.method_id,len(node.method_args))
            node.computed_type = class_method.return_type
        except Exception as e:
            self.errors.append(e.args[0])