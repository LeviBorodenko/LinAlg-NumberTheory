from fractions import Fraction  # Needed for exact results
import unittest

class row(object):
    """A row of a matrix.
    You can add, dot multiply and scalar multiply them
    and two rows are equal if they are collinear."""

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

    def __radd__(self, other):
        return self + other

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

    def __setitem__(self, key, item):
        if type(item) in [int, float, Fraction] and type(key) == int:
            self.val[key] = Fraction(item)
        else:
            print("Invalid assignment")


class matrix(object):
    """[summary]
    example: N = matrix([ [1, 2], [3, 4]])
    N now represents a matrix object that you can perform
    various operations on.
    [description]
    Initialized by a list of rows - rows being lists of numbers -
    you can add, multiply, exponentiate, reduce them etc.
    Have fun
    Variables:
        self.n - number of rows
        self.m - number of columns
        self.val - list containing the rows
    """

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

    def __len__(self):
        return len(self.val)

    def __add__(self, other):
        if [self.n, self.m] != [other.n, other.m]:
            print("Can only add matrices of same dimensions")
        else:
            return matrix([self[i] + other[i] for i in range(len(self))])

    def __neg__(self):
        return matrix([-i for i in self.val])

    def __sub__(self, other):
        return self + (- other)

    def __mul__(self, other):
        if type(other) in [int, float, Fraction]:
            return matrix([other * i for i in self.val])
        elif type(other) == matrix and self.m == other.n:
            result = []
            for i in range(self.n):
                newRow = row([0] * other.m)
                for j in range(self.m):
                    newRow += self[i][j] * other[j]
                result.append(newRow)
            return matrix(result)
        else:
            print("Invalid Multiplication")
            return None

    def __rmul__(self, other):
        if type(other) in [int, float, Fraction]:
            return matrix([other * i for i in self.val])

    def __setitem__(self, key, item):
        if type(item) in [list, row] and type(key) == int:
            self.val[key] = row(item)
        else:
            print("Invalid Assignment")

    def mul(self, Row, Factor):
        self[Row] *= Fraction(Factor)
        return self

    def prm(self, index, outdex):
        temp = self[outdex]
        self[outdex] = self[index]
        self[index] = temp
        return self

    def add(self, index, target):
        self[target] += self[index]
        return self

    def colReduce(self, col):
        """[summary]
        Performs extended Gaussian elimination on the
        col'th column.
        [description]
        Returns a Matrix that when left multiplied with
        self makes all entries in the col'th column
        0 except for the entry that lies on the diagonal
        - that one will become 1.
        If column does not have a pivot colReduce
        returns identity.
        Arguments:
            col {[int]} -- index of column to reduce

        Returns:
            [matrix] -- products of elem. ROPs
        """
        temp = self
        n = self.n
        U = I(n)

        for i in range(col, n):
            if self[i][col] != 0:
                pivot = [i, self[i][col]]
                break
        else:
            return U

        U = U.mul(pivot[0], 1 / pivot[1])
        temp = U * temp
        for i in range(n):
            if i != pivot[0] and temp[i][col] != 0:
                U = U.mul(pivot[0], -temp[i][col]).add(pivot[0],
                                                       i).mul(pivot[0], -1 / temp[i][col])
                temp = U * temp
            U = U.prm(pivot[0], col)
        return U

    def inverse(self):
        """[summary]
        Returns the inverse of self.
        [description]
        The inverse is found using elem ROPs.
        If no inverse exists then .inverse() is the
        matrix that when multiplied with self gives
        the row reduced echelon form.
        Returns:
            [matrix] -- inverse
        """
        if self.isSquare:
            n = self.n
            temp = self
            U = I(n)
            for i in range(n):
                U = temp.colReduce(i) * U
                temp = temp.colReduce(i) * temp
            return U
        else:
            print("Matrix non Square")
            n = self.n
            temp = self
            U = I(n)
            for i in range(n):
                U = temp.colReduce(i) * U
                temp = temp.colReduce(i) * temp
            return U

    def __pow__(self, expo):
        if expo == 0:
            return I(self.n)
        elif int(expo) != expo:
            print("only integer exponents, please!")
            return False
        elif expo > 0:
            P = self
            A = self
            for i in range(expo - 1):
                P = P * A
            return P
        elif expo < 0:
            temp = self.inverse()
            return temp.__pow__(-expo)

    def __eq__(self, other):
        if type(other) == matrix:
            if [self.n, self.m] == [other.n, other.m]:
                for i in range(self.n):
                    for j in range(self.m):
                        if self[i][j] != other[i][j]:
                            return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def numbZeroRows(self):
        temp = row([0] * self.m)
        counter = 0
        for i in self.val:
            if i == temp:
                counter += 1
        return counter

    def rank(self):
        """[summary]
        Gives the rank of self.
        [description]
        It counts the zero rows in the echelon
        form of self.
        Returns:
            [int] -- rank
        """
        return self.n - (self.inverse() * self).numbZeroRows()

    def rowReduce(self):
        """[summary]
        Returns echelon form.
        [description]
        Using elem. ROPs.

        Returns:
            [matrix] -- echelon from of self
        """
        return self.inverse() * self


def vector(lst):
    if False in [type(i) in [int, float, Fraction] for i in lst]:
        print("Vector must be a list of numbers")
    else:
        return matrix([[i] for i in lst])


def I(dim):
    """[summary]
    Gives the dim x dim identity matrix.

    Arguments:
        dim {[int]} -- dimension

    Returns:
        [matrix] -- identity
    """
    mx = []
    for i in range(dim):
        mx.append([0] * i + [1] + [0] * (dim - i - 1))
    return matrix(mx)


def test():
    
    print("lol")

if __name__ == "__main__":
    test()
