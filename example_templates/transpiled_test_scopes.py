s = 0
def first(f):
    s = f
    def second(f):
        return (s + f)
    return second(10)
print(first(5))
print(s)