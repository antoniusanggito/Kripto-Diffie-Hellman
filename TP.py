# Coret-coret TP
from random import randrange

# Could use gmpy2 for faster big number processing
import gmpy2
def num(n):
    return gmpy2.mpz(n)

## Finding q
# Miller-Rabin Primality Test
# https://stackoverflow.com/questions/17298130/working-with-large-primes-in-python
def is_prime_miller_rabin(n, t=10):
    # Cek genap
    if (not n & 1):
        return False

    # Setup (n-1) = 2^k * q
    k = 0
    q = n-1
    while (q % 2 == 0):
        q >>= 1
        k += 1

    # Algo pengecekan
    def check(a, k, q, n):
        x = pow(a, q, n)
        if x == 1:
            return True
        for _ in range(k-1):
            if x == n-1:
                return True
            x = pow(x, 2, n)
        return x == n-1

    # Cek sebanyak t kali dengan a random beda
    for _ in range(t):
        a = randrange(2, n-1)
        if not check(a, k, q, n):
            return False
    return True

def next_prime(n):
    # Cek genap
    if (not n & 1):
        n += 1

    # Cek primality test setiap bilangan ganjil setelahnya
    while True:
        print(n, flush=True)
        if is_prime_miller_rabin(n):
            break
        n += 2
    return n

# Randomize 20-25 digit
random_q = num(randrange(10000000000000000000, 10000000000000000000000000)) 
print('Init random q:', random_q)
q = next_prime(random_q)
# q = next_prime(num(4821400796452833382408514)) # contoh edge case faktor: 2, 196873223, 12244937942761351, wheel cepet
# q = next_prime(num(9187872044499284894799247)) # contoh edge case faktor: 7243, 23491064283009610543, 2, 3, wheel lama
print('q:', q)

## Finding a
def is_primitive_root(fs, n, q):
    phi = q-1
    for it in fs:
        if (pow(n, phi // it, q) == 1):
            return False
    return True

# Trial Division with Wheel Factorization (2,3,5,7)
# https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/
# https://cp-algorithms.com/algebra/factorization.html#wheel-factorization
def factors_trial_division_wheel(n) :
    fs = set()

    # Faktorkan 2,3,5,7 dulu
    for d in [2, 3, 5, 7]:
        while (n % d == 0) :
            fs.add(num(d))
            n = n // d
    inc = [2,4,2,4,6,2,6,4,2,4,6,6,2,6,4,2,6,4,6,8,4,2,4,2,4,8,6,4,6,2,4,6,2,6,6,4,2,4,6,2,6,4,2,4,2,10,2,10] # wheel increment pattern 2,3,5,7

    # Trial division dengan inc
    i = 0
    d = num(11)
    prime_checked_flag = False
    while (d*d <= n):
        if (not prime_checked_flag):
            if is_prime_miller_rabin(n):
                print('PRIME!', n, flush=True)
                break
            else:
                print('NOT PRIME, KEEP CLIMBING', n, flush=True)
                prime_checked_flag = True
        while (n % d == 0) :
            fs.add(num(d))
            n = n // d
            prime_checked_flag = False
        if (i == 48): i = 0
        d += inc[i]
        i += 1

    if (n > 1) :
        fs.add(n)
    return fs

# # Precompute Primes, no factorization
# # https://cp-algorithms.com/algebra/factorization.html#precomputed-primes
# def factors_precompute_primes(n):
#     fs = set()

#     # Buka file list primes <= 193617751 (sqrt(37487833502298001))
#     with open('./primes.txt', 'r') as f:
#         primes = f.read().split(' ')
#         primes.pop()
#         primes = list(map(int, primes))

#     # Trial division dengan precomputed primes
#     for d in primes:
#         if (d*d > n):
#             break
#         while (n % d == 0):
#             fs.add(num(d))
#             n = n // d

#     if (n > 1) :
#         fs.add(num(n))

#     return fs

def next_primitive_root(n, q):
    fs = factors_trial_division_wheel(q-1)    # trial division with wheel
    # fs = factors_precompute_primes(q-1)         # precompute primes
    print('Prime factor:', fs)

    # Cek primitive root satu persatu
    while n < q:
        print(n, flush=True)
        if is_primitive_root(fs, n, q):
            return n
        n += 1

# Cari a dimulai dari 2
a = next_primitive_root(num(2), q)
print('a:', a)

# Input private key
xA = num(int(input("\nPrivate Key Alice: "))) # xA >= 10 digit < q-1
xB = num(int(input("Private Key Bob: "))) # xB >= 10 digit < q-1

# Penghitungan public key
yA = pow(a, xA, q)
yB = pow(a, xB, q)
print("Public Key Alice:", yA)
print("Public Key Bob:", yB)

# Penghitungan secret key
kA = pow(yB, xA, q)
kB = pow(yA, xB, q)
print("Secret Key Alice:", kA)
print("Secret Key Bob:", kB)