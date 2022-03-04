from simulation.simulation import *
from simulation.customer import *
from compilation.language.built_ins import *
from simulation.Genetic_algorithm import MakeSim
def fibonacci(f):
    p = 1
    s = 1
    i = 0
    while (i <= (f - 2)):
        temp = p
        p = s
        s = (s + temp)
        i = (i + 1)
    return s
def rec_fibonacci(f):
    if (( f == 0 ) or ( f == 1 )):
        return 1
    return (rec_fibonacci((f - 1)) + rec_fibonacci((f - 2)))
def factorial(a):
    s = 1
    result = 1
    if ( a < 2 ):
        a = 1
    else:
        while ( s < a ):
            result = (result * a)
            a = (a - 1)
        result = result
    return result
def rec_factorial(a):
    if ( a < 2 ):
        return 1
    return (a * rec_factorial((a - 1)))
print((( rec_fibonacci(5) == fibonacci(5) ) and ( fibonacci(5) == 8 )))
print((( factorial(5) == rec_factorial(5) ) and not ( factorial(5) != 120 )))