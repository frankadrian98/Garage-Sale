
from language.types import *



Classes = {

    'Main': [
    Method('create_Agent', 'Agent', [], []),
    ] ,
    'Agent':[
    Attribute('id',NumberType()),
    Attribute('model',AnyType()),
    Method('sim', 'void', [], []),
    ],
}

def get_members(_type):
    res = []
    global Classes
    for member in Classes[_type]:
        res.append(member)
    
    return res