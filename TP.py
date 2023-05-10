# Coret-coret TP
import math
from random import randrange

# Could use gmpy2 for faster big number processing
import gmpy2
def num(n):
    return gmpy2.mpz(n)

# Miller-Rabin
# https://stackoverflow.com/questions/17298130/working-with-large-primes-in-python
def is_prime(n, k=10):
    if n == 2:
        return True
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True

def next_prime(num):
    if (not num & 1) and (num != 2):
        num += 1
    while True:
        print(num, flush=True)
        if is_prime(num):
            break
        num += 2
    return num

# q = num(30548218132221098119)
random_q = num(randrange(10000000000000000000, 999999999999999999999999999999)) # random 20-30 digit
print('Init random q:', random_q)
q = next_prime(random_q)
print('q:', q)

# Utility function to store prime factors of a number
# https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/
def findPrimefactors(s, n) :
    while (n % 2 == 0) :
        s.add(num(2))
        n = n // 2

    for i in range(3, int(math.sqrt(n))+1, 2):
        print(i, flush=True)
        while (n % i == 0) :
            s.add(num(i))
            n = n // i

    if (n > 2) :
        s.add(n)

def is_primitive_root(s, num, q):
    phi = q-1
    for it in s:
        if (pow(num, phi // it, q) == 1):
            return False
    return True

from sympy.ntheory import factorint
def next_primitive_root(num, q):
    # s = set()
    # findPrimefactors(s, q-1)
    s = set(factorint(q-1).keys()) # prime factorization using fast library
    print('Prime factor:', s)

    start = num
    while num < q:
        print(num, flush=True)
        if is_primitive_root(s, num, q):
            return num
        num += 1
    num = start-1
    while num > 0:
        print(num, flush=True)
        if is_primitive_root(s, num, q):
            return num
        num -= 1

# a = num(26709239175572505459)
random_a = num(randrange(1, q-1))
print('\nInit random a:', random_a)
a = next_primitive_root(random_a, q)
print('a:', a)

xA = num(int(input("\nPrivate Key Alice: "))) # xA >= 10 digit < q-1
xB = num(int(input("Private Key Bob: "))) # xB >= 10 digit < q-1

# Using pow() works fast enough, even 20digit^10digit++
yA = pow(a, xA, q)
yB = pow(a, xB, q)

print("Public Key Alice:", yA)
print("Public Key Bob:", yB)

kA = pow(yB, xA, q)
kB = pow(yA, xB, q)

print("Secret Key Alice:", kA)
print("Secret Key Bob:", kB)