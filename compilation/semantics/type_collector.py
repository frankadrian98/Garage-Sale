
from compilation.tools import visitor
from compilation._parser.ast_nodes import ProgramNode
from compilation.language.types import Method,Attribute
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
        Garage_Sale_Model = self.typecontext.create_type('Garage_Sale_Model')
        worker = self.typecontext.create_type('Worker')
        make_sim = self.typecontext.create_type('MakeSim')

        main.define_method('print', void, ['text'], [_any])
        main.define_method('l_append',void,['list','elem'],[_list,_any])
        main.define_method('l_remove',void,['list','elem'],[_list,_any])
        main.define_method('l_len',_int,['list'],[_list])
        main.define_method('randint',_int,['from','to'],[_int,_int])
        main.define_method('Customer', customer, ['id'], [_int])
        main.define_method('Server', server, ['id'], [_int])
        main.define_method('Cashier', cashier, ['id'], [_int])
        main.define_method('Garage_Sale_Model', Garage_Sale_Model, ['no_costumers','no_servers','no_cashiers'], [_int,_int,_int])
        main.define_method('Garage_Sale_Model', Garage_Sale_Model, [], [])
        main.define_method('print_sim_data',void,['gsm','no_servers','no_cashiers'],[Garage_Sale_Model,_int,_int])
        main.define_method('MakeSim', make_sim, [], [])

        Garage_Sale_Model.define_method('add_customer',void,[],[])
        Garage_Sale_Model.define_method('remove_customer',void,['id'],[_int])
        Garage_Sale_Model.define_method('add_server',void,[],[])
        Garage_Sale_Model.define_method('remove_server',void,['id'],[_int])
        Garage_Sale_Model.define_method('add_cashier',void,[],[])
        Garage_Sale_Model.define_method('remove_cashier',void,['id'],[_int])
        Garage_Sale_Model.define_method('sim',void,[],[])
        Garage_Sale_Model.define_method('get_total_gain',_int,[],[])
        Garage_Sale_Model.define_attribute('no_servers',_int)
        Garage_Sale_Model.define_attribute('no_cashiers',_int)
        Garage_Sale_Model.define_attribute('no_customers',_int)
        Garage_Sale_Model.define_attribute('time',_int)
        Garage_Sale_Model.define_attribute('no_cashiers',_int)
        Garage_Sale_Model.define_attribute('cashiers',_list)
        Garage_Sale_Model.define_attribute('servers',_list)
        Garage_Sale_Model.define_attribute('customers',_list)


        customer.define_attribute('id',_int)

        worker.define_attribute('service_time',_int)
        worker.define_attribute('id',_int)
        worker.define_attribute('queue',_list)
        

        make_sim.define_method('callgenetic',void,['count'],[_int])