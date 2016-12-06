from fractions import Fraction


class row(object):
    """docstring for row"""

    def __init__(self, lst):
        super(row, self).__init__()
        if type(lst) == row:
            self.val = [Fraction(i) for i in lst]

        elif type(lst) != list or False in [type(i) == int or type(i) == float or type(i) == Fraction for i in lst]:
            print("Row must be a list of numbers")
            self.val = "None"
        else:
            self.val = [Fraction(i) for i in lst]

    def __repr__(self):
        return str([float(i) for i in self.val])

    def __len__(self):
        return len(self.val)

    def __getitem__(self, key):
        return self.val[key]

    def __add__(self, other):
        if len(self) != len(other):
            print("Can only add rows of same size")
        else:
            Sum = []
            for index in range(len(self)):
                Sum.append(self[index] + other[index])
            return row(Sum)

    def __sub__(self, other):
        return self + (- other)

    def __mul__(self, other):  # default Left Multiplication (so)
        if type(other) in [float, int, Fraction]:
            return row([Fraction(other) * i for i in self.val])
        elif type(other) == row:
            return row([self[i] * other[i] for i in range(len(self))])

    def __rmul__(self, other):  # if default fails Right Multiplication (os)
        if type(other) in [float, int, Fraction]:
            return row([Fraction(other) * i for i in self.val])

    def firstNonZero(self):
        """Returns [index, and value of first pivot]
                And "ZeroRow" if no pivot is found"""
        for index, value in enumerate(self.val):
            if value != 0:
                return [index, value]
        else:
            return "ZeroRow"

    def __str__(self):
        return str([float(i) for i in self.val])

    def __neg__(self):
        return row([-self[i] for i in range(len(self))])

    def __eq__(self, other):
        if self.firstNonZero() == other.firstNonZero() == "ZeroRow":
            return True
        elif self.firstNonZero() == "ZeroRow":
            return False
        elif other.firstNonZero() == "ZeroRow":
            return False
        else:
            k = self.firstNonZero()[1] / other.firstNonZero()[1]
            temp = k * other
            if self.val == temp.val:
                return True
            else:
                return False


class matrix(object):
    """docstring for matrix"""

    def __init__(self, lst):
        super(matrix, self).__init__()

        if False in [type(i) == row or type(i) == list for i in lst]:
            print("Invalid initialization input")

        elif False in [len(lst[0]) == len(lst[i]) for i in range(len(lst))]:
            print("All rows must have the same length")

        else:
            self.val = [row(lst[i]) for i in range(len(lst))]
            self.n = len(self.val)
            self.m = len(self.val[0])
            if self.n == self.m:
                self.isSquare = True
            else:
                self.isSquare = False

    def __repr__(self):
        rep = ""
        for i in self.val:
            rep += str(i) + "\n"
        return rep

    def __getitem__(self, key):
        return self.val[key]


def test():
    a = 2 * row([1, 2, 3, 4])
    b = 4 * row([1, 2, 3, 4])
    M = matrix([a, b])
    print(M[0][1])


if __name__ == "__main__":
    test()
