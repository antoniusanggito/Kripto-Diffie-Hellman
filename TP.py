# Coret-coret TP
from random import randrange

# Could use gmpy2 for faster big number processing
import gmpy2
def num(n):
    return gmpy2.mpz(n)

## Finding q
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

random_q = num(randrange(10000000000000000000, 99999999999999999999)) # random 20-30 digit
print('Init random q:', random_q)
q = next_prime(random_q)
# q = next_prime(num(9131957573541077876047273))
print('q:', q)

## Finding a
def is_primitive_root(s, num, q):
    phi = q-1
    for it in s:
        if (pow(num, phi // it, q) == 1):
            return False
    return True

# Wheel Factorization with Pollard's Rho? (wrong result)
# https://stackoverflow.com/questions/51533621/prime-factorization-with-large-numbers-in-python
def factors(n, b1=10000): # 2,3,5-wheel, then rho
    wheel = [1,2,2,4,2,4,2,4,6,2,6]
    w, f, fs = 0, 2, set()
    # while f*f <= n and f < b1:
    while f*f <= n:
        while n % f == 0:
            fs.add(num(f))
            n /= f
        f, w = f + wheel[w], w+1
        if w == 11: w = 3
    if n == 1: return fs
    fs.add(num(n))
    return fs

# Trial Division with Wheel Factorization (2, 3, 5)
# https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/
# https://cp-algorithms.com/algebra/factorization.html#wheel-factorization
def factors_trial_division_wheel235(n) :
    s = set()
    for d in [2, 3, 5]:
        while (n % d == 0) :
            s.add(num(d))
            n = n // d
    inc = [4, 2, 4, 2, 4, 6, 2, 6] # wheel increment pattern
    i = 0
    d = 7
    while (d*d <= n):
        while (n % d == 0) :
            s.add(num(d))
            n = n // d
        if (i == 8): i = 0
        d += inc[i]
        i += 1
    if (n > 1) :
        s.add(n)
    return s

# # Pollard's Rho (not working, only for 1 factor)
# # https://stackoverflow.com/questions/22827876/optimizing-a-prime-number-factorization-algorithm
# def factors_pollard_rho(n, c):
#     f = lambda x: (x*x+c) % n
#     t, h, d = 2, 2, 1
#     while d == 1:
#         t = f(t); h = f(f(h)); d = math.gcd(t-h, n)
#     if d == n:
#         return factors_pollard_rho(n, c+1)
#     return d

def next_primitive_root(num, q):
    s = factors_trial_division_wheel235(q-1)    # trial division with wheel
    # s = factors(q-1)                          # wheel with rho factorization?
    print('Prime factor:', s)

    while num < q:
        print(num, flush=True)
        if is_primitive_root(s, num, q):
            return num
        num += 1

a = next_primitive_root(2, q)
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