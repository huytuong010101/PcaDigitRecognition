class HandleMatrix:
    @staticmethod
    def mul2matrix(a, b):
        if len(a[0]) != len(b):
            raise ValueError("Matrix not valid")
        ans = []
        rowA = len(a)
        columnA = len(a[0])
        columnB = len(b[0])
        for i in range(rowA):
            rowAns = []
            for j in range(columnB):
                sum = 0
                for k in range(columnA):
                    sum += a[i][k] * b[k][j]
                rowAns.append(sum)
            ans.append(rowAns)
        return ans

    @staticmethod
    def mulNumberAndMatrix(n, a):
        ans = []
        for row in a:
            ans.append([item * n for item in row])
        return ans

    @staticmethod
    def T(a):
        ans = []
        row = len(a)
        column = len(a[0])
        for i in range(column):
            rowAns = []
            for j in range(row):
                rowAns.append(a[j][i])
            ans.append(rowAns)
        return ans

    @staticmethod
    def mean(a):
        row = len(a)
        column = len(a[0])
        ans = []
        for i in range(column):
            sum = 0
            for j in range(row):
                sum += a[j][i]
            ans.append(sum / row)
        return ans

    @staticmethod
    def centreToZero(a, mean):
        ans = []
        for row in a:
            rowAns = []
            for index, value in enumerate(row):
                rowAns.append(value - mean[index])
            ans.append(rowAns)
        return ans

    @staticmethod
    def printMatrix(a):
        for row in a:
            print(row)
