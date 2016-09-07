import timeit
# import gmpy2
import math
import itertools
import fractions


# def isSquare(n):
#     return gmpy2.isqrt(n) ** 2 == n


class continuedFraction(object):
    """Continued Fraction for Sqrt(D)"""
    def __init__(self, D):
        super(continuedFraction, self).__init__()
        self.D = D
        self.sD = math.sqrt(D)
        self.coeffs = self.getCoeff()

    def getCoeff(self):
        c = math.floor(self.sD)
        Rest = 1 / (self.sD - math.floor(self.sD))
        coeff = [c]
        Rests = [Rest]
        while True:
            c = math.floor(Rest)
            Rest = 1 / (Rest - c)
            coeff.append(c)
            if round(Rest, 4) in Rests:
                del coeff[-1]
                return coeff
            else:
                Rests.append(round(Rest, 4))

    def getConvQ(self, n):
        coeffs = self.coeffs[1::]
        Q = 1
        q = 0
        counter = 1
        if n == -1:
            return q
        elif n == 0:
            return Q
        for a in itertools.cycle(coeffs):
            if counter == n:
                return Q
            temQ = Q
            Q = a * Q + q
            q = temQ
            counter += 1

    def getConvP(self, n):
        coeffs = self.coeffs[1::]
        P = self.coeffs[0]
        p = 1
        counter = 1
        if n == -1:
            return p
        elif n == 0:
            return P
        for a in itertools.cycle(coeffs):
            if counter == n:
                return P
            temP = P
            P = a * P + p
            p = temP
            counter += 1

    def getConvergentValue(self, n):
        return self.getConvP(n) / self.getConvQ(n)

    def getUnit(self):  # P^2 - D Q^2 = +- 1
        n = 1
        P = self.getConvP(n)
        Q = self.getConvQ(n)
        while True:
            if P ** 2 - self.D * (Q ** 2) == 1 or P ** 2 - self.D * (Q ** 2) == -1:
                a = ZsD(P, Q, self.D)
                print a
                return a
            elif Q ** 2 - self.D * (P ** 2) == 1 or Q ** 2 - self.D * (P ** 2) == -1:
                a = ZsD(Q, P, self.D)
                print a
                return a
            n += 1
            P = self.getConvP(n)
            Q = self.getConvQ(n)
            if n > 500:
                return "Sorry! No solution found."


class ZsD(object):
    """Element of Z[sqrt(D)]"""
    def __init__(self, a, b, D):
        super(ZsD, self).__init__()
        self.a = int(a)
        self.b = int(b)
        self.D = int(D)
        self.val = [int(a), int(b)]
        self.norm = int(a)**2 - int(D) * int(b) ** 2
        self.rep = str(a) + " + " + str(b) + "sqrt(" + str(D) + ")"

    def __str__(self):
        return str(self.a) + " + " + str(self.b) + "sqrt(" + str(self.D) + ")"

    def __add__(self, other):
        if self.D == other.D:
            return ZsD(self.a + other.a, self.b + other.b, self.D)
        else:
            print "Not in the same ring!"

    def __sub__(self, other):
        if self.D == other.D:
            return ZsD(self.a - other.a, self.b - other.b, self.D)
        else:
            print "Not in the same ring!"

    def __mul__(self, other):
        if self.D == other.D:
            return ZsD(self.a * other.a + self.D * self.b * other.b, self.a * other.b + self.b * other.a, self.D)
        else:
            print "Not in the same ring!"

    def __pow__(self, power):
        power = int(power)
        if power < 0:
            return "Only positive exponents!"
        elif power == 0:
            return ZsD(1, 0, self.D)
        else:
            M = self
            for i in range(1, power):
                M *= self
            return M


class PythTrip(object):
    """Represents a Pythagorean Triple based on two coprime numbers (n,m)"""
    def __init__(self, M, N):
        super(PythTrip, self).__init__()
        self.gcd = 1  # fractions.gcd(M, N)
        self.n = int(N / self.gcd)
        self.m = int(M / self.gcd)
        self.a = self.m ** 2 - self.n ** 2
        self.b = 2 * self.m * self.n
        self.c = self.m ** 2 + self.n ** 2
        self.p = self.a + self.b + self.c
        self.area = (self.a * self.b) / 2
        self.val = [self.a, self.b, self.c]

    def __str__(self):
        return str(self.val)

    def nonUniqueUpToCertainP(self, P):  # Returns the # of PTs with k(a+b+c)<P
        f = P / self.p
        if f == 1:
            return 0
        if int(f) == f:
            return int(f) - 1
        else:
            return int(f)

    def eulerProblemCheck(self):
        if self.c % abs(self.a - self.b) == 0:
            return True
        else:
            return False


def coprimeTuples(mMax):
    # Returns all Tuples (m,n) s.t. (m,n) = 1 and m > n
    lst = []
    for m in xrange(2, mMax + 1):
        if m <= 5000:
            for n in xrange(1, m):
                if fractions.gcd(m, n) == 1:
                    lst.append([m, n])
        else:
            for n in xrange(1, int((50000000 - m ** 2) / m) + 1):
                if fractions.gcd(m, n) == 1:
                    lst.append([m, n])
    return lst


def main():
    Tuples = coprimeTuples(7071)
    S = 0
    for i in Tuples:
        a = PythTrip(i[0], i[1])
        if a.eulerProblemCheck():
            S += a.nonUniqueUpToCertainP(100000000)
    print S

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    print "Runtime: " + str(timeit.default_timer() - start)  # Outputs runtime
