from typing import List

class Attribute:
    def __init__(self,name,_type):
        self.name = name
        self.type = _type

class Method:
    def __init__(self,name,return_type,arguments,argument_types):
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        self.argument_types = argument_types
    
    def equal_types(self,self_types,other_types):
        for i in range(len(self_types)):
            if self_types[i]!=other_types[i] and self_types[i].name != 'any' and other_types[i].name != 'any':
                return False
        return True

    def __eq__(self, other):
        return other.name == self.name and other.return_type == self.return_type and len(other.arguments)==len(self.arguments) and self.equal_types(self.argument_types,other.argument_types)

class Type:
    def __init__(self,name):
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.content_type = None

    def get_attribute(self,name: str) -> 'Attribute':
        if name in self.attributes:
            return self.attributes[name]       
        else:
            raise Exception(self.name + ' has no attribute '+ name)

    
    def get_method(self,name: str, args:int) -> 'Method':
        if (name,args) in self.methods:
            return self.methods[(name,args)]       
        else:
            raise Exception(self.name + ' class has no method '+ name + '() with '+ str(args) + ' args')

    def define_attribute(self,name:str, _type: 'Type') -> bool :

        if name in self.attributes:
            return False
        
        self.attributes[name] = Attribute(name, _type)
        return True


    def define_method(self,name: str, return_type: 'Type', arguments: List[str], argument_types: List['Type']) -> bool:
      
        if (name,len(arguments)) in self.methods:
            return False
        
        self.methods[(name,len(arguments))] = Method(name,return_type,arguments,argument_types)
        return True

    def __eq__(self,other):
        return other and self.name == other.name

    def __ne__(self,other):

        return other and self.name != other.name

    def __str__(self):
        return self.__qualname__


class NumberType(Type):
    def __init__(self):
        super().__init__('number')

class StringType(Type):
    def __init__(self):
        super().__init__('string')

class BooleanType(Type):
    def __init__(self):
        super().__init__('bool')

class VoidType(Type):
    def __init__(self):
        super().__init__('void')

class ListType(Type):
    def __init__(self):
        super().__init__('list')
        


class AnyType(Type):
    def __init__(self):
        super().__init__('any') 
    
    def __eq__(self,other):
        return True

    def __ne__(self,other):
        return False

class UnknownType(Type):
    def __init__(self):
        super().__init__('unknown') 
    
    def __eq__(self,other):
        return False

    def __ne__(self,other):
        return True