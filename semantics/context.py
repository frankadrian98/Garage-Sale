
from language.types import Type
from typing import List


class Variable:
    def __init__(self,name,_type):
        self.name = name
        self.type = _type


class Function:
    def __init__(self,name,return_type,args,arg_types,checked_type=None):
        self.name = name
        self.return_type = return_type
        self.arguments = args
        self.argument_types = arg_types


class Context:

    def __init__(self,parent = None):
        self.parent =parent
        self.vars = {}
        self.funs = {}

    
    def get(self,id) -> Variable:
        if id in self.vars:
            return self.vars[id]

        if self.parent:
            return self.parent.get(id)
        
        raise Exception(id + ' is not defined in current context')

    def get_fun(self,id,args) -> Function:
        if (id,args) in self.funs:
            return self.funs[(id,args)]
        if self.parent:
            return self.parent.get_fun(id,args)

        raise Exception(id + '() is not defined in current context')

    def check_var(self,var: str) -> bool:
        if var in self.vars:
            return True       
        if self.parent:
            return self.parent.check_var(var)        
        return False

    def define_var(self,var: str,_type: 'Type') -> bool:
        if self.check_var(var):
            return False
        self.vars[var] = Variable(var,_type)
        return True

    def define_local_var(self,var: str,_type: 'Type') -> bool:
        if var in self.vars:
            return False 
        self.vars[var] = Variable(var,_type)
        return True

    def check_fun(self, fun: str, args: int):
        if (fun, args) in self.funs:
            return True
        return False
    
    def define_fun(self, fun: str, return_type: 'Type', args: List[str], arg_types: List['Type']) -> bool:
        if not self.check_fun(fun, len(args)):
            self.funs[(fun, len(args))] = Function(fun, return_type, args, arg_types)
            return True
        return False

    def create_child_context(self):
        return Context(self)

class TypeContext:
    
    def __init__(self,parent = None):
        self.parent = parent
        self.types = {}
        self.funs = {}

    def create_type(self,name: str) -> 'Type':
        if name in self.types:
            raise Exception(name + ' Type was already defined in current context')
        else:
            _type = Type(name)
            self.types[name] = _type
            return _type

    def get_type(self,name: str) -> 'Type':
        if name in self.types:
            return self.types[name]
        raise Exception(name + ' Type isn\'t defined in current context')
        
    
    
    

    def create_child_context() -> 'TypeContext':
        return TypeContext(self)
    