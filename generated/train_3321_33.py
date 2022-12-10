# evil(n) returns "It's Evil!" if n is an evil number, otherwise it returns "It's Odious!" The range of evil is the set of all integers, and the domain is the set of all strings.
def evil(n):
    gen = evilometer(n)
    if sum(list(gen)) % 2 == 0:
        return "It's Evil!"
    else:
        return "It's Odious!"

# evilometer(n) is a generator that yields n times if n is even, and yields n // 2 times if n is odd.
def evilometer(n):
    while n:
        yield n
        if n % 2:
            n //= 2
        else:
            n -= 1


assert evil(1) == "It's Odious!"
assert evil(2) == "It's Odious!"
assert evil(3) == "It's Evil!"

