from collections import deque
from typing import Union, Callable


from compilation._lexer.token_ import Token, TokenRegex


#Crea una regla gramatical con los parametros pare crear el ast
def rule(rule_string: str, name: Union[str, None], process: Callable, antilookahead=[]):
    rule = []
    rule_string = rule_string.split() #Separar el la regla en terminales y no terminales
    rule.append(rule_string.pop(0)) #Lado izquierdo de la regla
    rule.append(rule_string)
    rule.append([name])
    rule.append(process)
    rule.append(antilookahead) #Definido en el Early's parse pero no utilizado
    return rule

def parse(grammar: dict, chart: dict, tokens, startrule: list):

    def make_tree(tree, process): #Utiliza la funcion lambda para crear el ast a partir de la lista de tokens
        return process(tree)

    def addto(curpos, val):  #Agrega el valor a la tabla sin repeticiones
        ref = val[:4]
        if ref not in reference[curpos]:
            chart[curpos].append(val)
            reference[curpos].append(ref)
            
    def closure(grammar, chart, token, curpos): #Agrega todas las reglas gramaticales a la posicion de la tabla que coincida con el no terminal pendiente
        for rule in grammar[token]:
            state = [rule[0],deque([]),deque(rule[1]),curpos,list(rule[2]),rule[3],rule[4]] 
            addto(curpos,state)

    def nextstate(state, element): #Retorna el nuevo estado a partir del actual y el proximo elemento a añadir al ast
        nextstate = [state[0],deque(state[1]),deque(state[2]),state[3],list(state[4]),state[5], state[6]] 
        shifted = nextstate[2].popleft() #Saca el primer elemento de la cola de los no vistos
        nextstate[1].append(shifted) #Lo anhade al final de los ya vistos
        nextstate[4].append(element)
        return nextstate

    def shift(tokens,chart,state,curpos):       #Matchea el token y avanza el estado hacia la posicion siguente de la tabla
        if tokens[curpos].type == state[2][0]:          #Si el token actual matchea con el proximo token del estado actual
            addto(curpos+1,nextstate(state,tokens[curpos].value)) #Genera el nuevo estado y y lo anhade al arbol

    def reduction(origin,chart,equal,curpos,tree):  #Completa el no terminal del estado finalizado y lo anhade en la posicion actual de la tabla
        for state in chart[origin]:                 #Chequea la tabla en la posicion del esado original
            if state[2] and state[2][0] == equal:   #Si el estado no no ha terminado y el token que le falta es el buscado, encontramos el estado original
                addto(curpos,nextstate(state,tree)) #Genera el nuevo estado modicando el original y lo anhade a la tabla
                

    reference = {}
    try:
        endline, endpos = tokens[-1].line, tokens[-1].col
    except:
        endline = endpos = 1000
    tokens.append(Token("endmarker",'eof',-1,-1,endline,endpos))
    for n in range(len(tokens)+1):
        chart[n] = []
        reference[n] = []
    chart[0].append([startrule[0],[],deque(startrule[1]),0,startrule[2],startrule[3],startrule[4]])

    for curpos in range(len(tokens)+1):
        if chart[curpos] == []:      #Si la tabla en la posicion actual esta vacia, no se hizo ningun shift valido
            curtoken = tokens[curpos-1]  
            raise Exception('\033[93m'+'Unexpected '+str(curtoken.value)+' at line '+str(curtoken.line)+' position '+str(curtoken.col)+'.'+'\033[0m')

  
        for state in chart[curpos]: #Por cada estado de la posicion actual
            equal = state[0] #Componentes del estado actual
            seen = state[1] 
            unseen = state[2]
            origin = state[3]
            tree = state[4]
            process = state[5]
            antilookahead = state[6]

            #Si llegamos al final de los tokens y estamos en el estado inicial pero ya finalizado, la cadena es valid
            if curpos == len(tokens)-1 and equal == startrule[0] and unseen == deque([]) and origin == 0:
                return make_tree(tree,process) #Retornamos el arbol

            #Si el estado finalizo y el estado no es antilookahead, finalizamos su arbol y le aplicamos reduction
            if not unseen:
                if tokens[curpos] not in antilookahead:
                    tree = make_tree(tree,process)
                    reduction(origin,chart,equal,curpos,tree)
                else:
                    continue
            elif unseen[0][0] >= 'A' and unseen[0][0] <= 'Z': #Si el estado pendiente es no terminal(Siempre mayusculas) aplicamos closure
                closure(grammar,chart,unseen[0],curpos)
            else:
                shift(tokens,chart,state,curpos) #Si es terminal le aplicamos shift


chart = {}       






