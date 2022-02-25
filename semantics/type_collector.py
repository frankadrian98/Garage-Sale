
from tools import visitor
from _parser.ast_nodes import ProgramNode
from language.types import Method,Attribute
class TypeCollector:

    def __init__(self,typecontext):
        self.typecontext = typecontext
   
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        _int = self.typecontext.create_type('int')
        _float = self.typecontext.create_type('float')
        string = self.typecontext.create_type('string')
        boolean = self.typecontext.create_type('bool')
        _list = self.typecontext.create_type('list')
        void = self.typecontext.create_type('void')
        _any = self.typecontext.create_type('any')
        main = self.typecontext.create_type('Main')
        agent = self.typecontext.create_type('Agent')
        server = self.typecontext.create_type('Server')
        customer = self.typecontext.create_type('Customer')
        cashier = self.typecontext.create_type('Cashier')
        main.define_method('print', void, ['text'], [_any])
        main.define_method('l_append',void,['list','elem'],[_list,_any])
        main.define_method('l_remove',void,['list','elem'],[_list,_any])
        main.define_method('l_len',_int,['list'],[_list])
        main.define_method('Agent', agent, ['id'], [_int])
        main.define_method('Customer', customer, ['id'], [_int])
        main.define_method('Server', server, ['id'], [_int])
        main.define_method('Cashier', cashier, ['id'], [_int])
        customer.define_method('sim',void,[],[])
        agent.define_attribute('id',_int)
        agent.define_method('sim',void,[],[])
