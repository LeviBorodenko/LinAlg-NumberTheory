from fractions import Fraction


class row(object):
    """Represents a row of a matrix.


    """

    def __init__(self, lst):
        super(row, self).__init__()
        self.val = [Fraction(i) for i in lst]
        self.len = len(lst)

    def __getitem__(self, index):
        return self.val[index]

    def __add__(self, other):
        Sum = []
        if self.len != other.len:
            print "Can't add rows of different dimensions"
            return False
        else:
            for index, value in enumerate(self.val):
                Sum.append(value + other.val[index])
        return row(Sum)

    def changeVal(self, index, value):
        self.val[index] = value

    def smul(self, scalar):  # Multiply every element of the row by a scalar
        try:
            int(scalar)
        except ValueError:
            print "Can only multiply with a scalar!"
            return False
        lst = []
        for i in self.val:
            lst.append(scalar * i)
        return row(lst)

    def __str__(self):
        return str([float(i) for i in self.val])

    def __len__(self):
        return len(self.val)

    def isZero(self):
        for i in self.val:
            if i != 0:
                return False
        else:
            return True


def Matrix(lst):
    mx = []
    l = len(lst[0])
    for i in lst:
        if len(i) != l:
            print "All rows must have the same number of elements!"
            return False
        else:
            mx.append(row(i))
    return matrix(mx)


class matrix(object):
    """Represent a Matrix

    [description]
        You can add'em, multiply'em, inverse'em and take powers of 'em!.
        So basically: All your heart desires!

    """

    def __init__(self, lst):
        super(matrix, self).__init__()
        self.val = lst
        self.rank = self.dim()[1]

    def __str__(self):
        string = ""
        for i in self.val:
            string += str(i) + "\n"
        return string

    def __add__(self, other):
        lst = []
        for index, Row in enumerate(self.val):
            lst.append(Row + other.val[index])
        return matrix(lst)

    def dim(self):
        """[summary]
        Gives the dimensions of the Matrix

        [description]
        Returns: [Number of columns, Number of Rows]
        """
        return [len(self.val[0]), len(self.val)]

    def __mul__(self, other):
        if self.dim()[0] != other.dim()[1]:
            print "Can't multiply those - wrong dimensions!"
            return False
        product = []
        for Row in self.val:
            newRow = row([0] * other.dim()[0])
            for index, factor in enumerate(Row):
                newRow = newRow + other.val[index].smul(factor)
            product.append(newRow)
        return matrix(product)

    def __pow__(self, expo):
        if expo == 0:
            return Unitmatrix(self.dim()[1])
        elif int(expo) != expo:
            print "only integer exponents, please!"
            return False
        elif expo > 0:
            P = self
            A = self
            for i in xrange(expo - 1):
                P = P * A
            return P
        elif expo < 0:
            temp = self.inverse()
            return temp.__pow__(-expo)

    def __getitem__(self, index):
        return self.val[index]

    def firstNonZeroEntry(self, col):
        """[summary]
        Finds the first non-zero entry on or below the diagonal
        and returns its [index, Value]

        [description]

        Arguments:
                col {[int]} -- what column should be scanned

        Returns:
                False -- If none found
                [index, Value] -- if match found
        """
        for i in xrange(col, self.rank):
            if self[i][col] != 0:
                return [i, self[i][col]]
        else:
            return False

    def colReduceMatrix(self, col):
        """[summary]
        Creates an echelon row reduced column of your matrix.
        [description]
        Basically: Gausselem + further reductions above the diagonal
        on a single column.
        Arguments:
                col {[int]} -- column that should be reduced

        Returns:
                False -- If not reducible
                Matrix -- if reducible [then it returns a Matrix
                                  mP such that mP * self = ReducedMatrix]
        """
        IndexValue = self.firstNonZeroEntry(col)
        mP = Unitmatrix(self.rank)
        if not IndexValue:
            return False

        else:
            temp = self
            mP = elemMatrixExchange(
                self.rank, IndexValue[0], 0) * mP
            mP = elemMatrixFactor(
                self.rank, 0, 1 / IndexValue[1]) * mP
            temp = mP * temp
            # print temp
            for i in range(1, self.rank):
                if temp[i][col] != 0:
                    mP = elemMatrixFactor(
                        self.rank, 0, - temp[i][col]) * mP
                    # print mP * self
                    mP = elemMatrixAdd(self.rank, 0, i) * mP
                    # print mP * self
                    mP = elemMatrixFactor(self.rank, 0, -1 / temp[i][col]) * mP
            mP = elemMatrixExchange(self.rank, 0, col) * mP
            return mP

    def inverse(self):
        """[summary]
        Returns the inverse of the matrix -- if it exists!
        [description]
        Looks for a series of elementary matrices that would
        reduce self to identity or to reach a state that does
        not allow any further reduction.
        Returns:
                False -- Not invertible
                Matrix -- Inverse
        """
        mP = Unitmatrix(self.rank)
        newMatrix = self
        for i in xrange(self.dim()[1]):
            temp = newMatrix.colReduceMatrix(i)
            if not temp:
                print "Not invertible!"
                return False
            else:
                newMatrix = temp * newMatrix
                mP = temp * mP
        return mP


def elemMatrixFactor(rank, index, factor):
    """[summary]
    returns an elementary matrix corresponding to
    the multiplication of the index'th row of a
    rank x n matrix by a factor given by "factor"


    Arguments:
            rank {[int]} -- number of rows
            index {[int]} -- index of the row that
                                             will be multiplied
            factor {[int, float, ...]} -- factor by which
                                                                    our row will be
                                                                    multiplied

    Returns:
            [Matrix] -- elementary matrix
    """
    U = Unitmatrix(int(rank))
    U[index].changeVal(index, factor)
    return U


def elemMatrixExchange(rank, index, outdex):
    """[summary]
    returns an elementary matrix corresponding
    to the the row operation of exchanging two 
    rows of a rank x n matrix
    [description]

    Arguments:
            rank {[int]} -- number of rows
            index {[int]} -- index of row that will be exchanged
            outdex {[int]} -- index of the other row

    Returns:
            [martix] -- elementary matrix
    """
    U = Unitmatrix(int(rank))
    U[index].changeVal(index, 0)
    U[index].changeVal(outdex, 1)

    U[outdex].changeVal(outdex, 0)
    U[outdex].changeVal(index, 1)

    return U


def elemMatrixAdd(rank, index, target):
    """[summary]
    Creates an elementary matrix that corresponds
    to the row operation of adding the index row
    to the target row.
    [description]

    Arguments:
            rank {int}      -- number of rows
            index {[int]}  -- index of the row that will be added
            target {[int]} -- index of the row that we will add
                                               the other row to.

    Returns:
            [matrix] -- elementary matrix
    """
    U = Unitmatrix(int(rank))
    U[target].changeVal(index, 1)
    return U


def createVector(lst):
    """[summary]
    Instead of typing:
            Matrix([[a], [b], [c], ...])
    you can now just call
            createVector([a, b, c, ...])
    and the function will return the same as the above.
                                    For the lazy.

    Arguments:
            lst {[list]} -- Entries of your vector

    Returns:
            1 by len(lst) Matrix
    """
    return Matrix([row([i]) for i in lst])


def Unitmatrix(rank):
    """[summary]
    creates a rank x rank unit matrix
    [description]

    Arguments:
            rank {int} -- side length 

    Returns:
            [matrix] -- Unit matrix
    """
    mx = []
    for i in range(rank):
        mx.append([0] * i + [1] + [0] * (rank - i - 1))
    return Matrix(mx)


def main():
    a = Matrix([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # y = createVector([1, 2, 3])
    print a.inverse()


if __name__ == '__main__':
    main()
