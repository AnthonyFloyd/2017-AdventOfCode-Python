def isprime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True

primeCounter = 0
counter = 0

for target in range(106700, 123717, 17):
    counter += 1
    if isprime(target):
        primeCounter += 1
        #print("Prime: {0:d}".format(target))

print("nPrimes: {0:d}".format(counter-primeCounter))
