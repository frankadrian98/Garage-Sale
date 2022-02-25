

class Node:
    pass

class ProgramNode(Node):
    def __init__(self,stml):
        self.stml = stml
        

class StatementListNode(Node):
    def __init__(self,statements):
        self.statements = statements

class FunDeclNode(Node):
    def __init__(self,_type,id,params,body):
        self.type = _type
        self.id = id
        self.arg_types = []
        self.args = []
        for tp in params:
            self.arg_types.append(tp[0])
            self.args.append(tp[1])
        self.body = body

class FunCallNode(Node):
    def __init__(self,id,args):
        self.id = id
        self.args = args
        self.computed_type= None

class ReturnNode(Node):
    def __init__(self,exp):
        self.exp = exp
        

class AssignNode(Node):
    def __init__(self,id, exp):
        self.id = id
        self.exp = exp

class DeclarationNode(Node):
    def __init__(self,_type,id,exp):
        self.type = _type
        self.id = id
        self.exp = exp

class InstanceDeclarationNode(Node):
    def __init__(self,_type,id,class_type,args):
        self.type = _type
        self.id = id
        self.class_type = class_type
        self.args = args

class LoopNode(Node):
    pass

class WhileNode(LoopNode):
    def __init__(self,cond,whileblock):
        self.cond = cond
        self.whileblock = whileblock

class ConditionalNode(Node):
    pass

class IfElseNode(ConditionalNode):
    def __init__(self,cond,ifblock,elseblock):
        self.cond = cond
        self.ifblock = ifblock
        self.elseblock = elseblock

class FlowNode(Node):
    pass

class ContinueNode(FlowNode):
    pass

class BreakNode(FlowNode):
    pass

class ListNode(Node):
    def __init__(self,content):
        self.content = content
        self.computed_type = None
        self.content_type = None

class ListIndexNode(Node):
    def __init__(self,exp,index):
        self.exp = exp
        self.index = index
        self.computed_type = None

class LiteralNode(Node):
    def __init__(self,value):
        self.value = value
        self.computed_type = None

class IntNode(LiteralNode):
    def __init__(self,value):
        super().__init__(value)
        self.type = 'int'

class FloatNode(LiteralNode):
    def __init__(self,value):
        super().__init__(value)
        self.type = 'float'

class StringNode(LiteralNode):
    def __init__(self,value):
        super().__init__(value)
        self.type = 'string'

class BooleanNode(LiteralNode):
    def __init__(self,value):
        super().__init__(value)
        self.type = 'bool'

class VoidNode(LiteralNode):
    def __init__(self,value):
        super().__init__(value)
        self.type = 'void'

class VariableNode(Node):
    def __init__(self,id):
        self.id = id
        self.computed_type = None

class NotNode(Node):
    def __init__(self,cond):
        self.cond = cond
        self.computed_type = None

class BinaryNode(Node):
    def __init__(self,left,operator,right):
        self.left = left
        self.operator = operator
        self.right = right
        self.computed_type = None

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class MultNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class AndNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

class GreatEqualNode(BinaryNode):
    pass

class LessEqualNode(BinaryNode):
    pass

class GreatNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class NotEqualNode(BinaryNode):
    pass

class AttributeNode(Node):

    def __init__(self,class_id,id):
        self.class_id = class_id
        self.id = id
        self.computed_type = None

class MethodCallNode(Node):
    
    def __init__(self,class_id,method_id,method_args):
        self.class_id = class_id
        self.method_id = method_id
        self.method_args=method_args
        self.computed_type = None

