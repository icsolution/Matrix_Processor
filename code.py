class Matrix:

    def __init__(self, matrix=None):
        self.matrix = [] if matrix is None else matrix
        self.rows = 0 if matrix is None else len(matrix)
        self.collum = 0 if matrix is None else len(matrix[0])
        self.result = []

    def create(self, name=None):
        if not name:
            self.rows, self.collum = input(f'Enter matrix size: ').split()
            print(f'Enter matrix:')
        else:
            self.rows, self.collum = input(f'Enter size of {name} matrix: ').split()
            print(f'Enter {name} matrix:')
        for i in range(int(self.rows)):
            self.matrix.append([int(i) if i.isdigit() else float(i) for i in input().split()])
        return self.matrix

    def __str__(self):
        return '\n'.join((' '.join(f'{i}' for i in row)) for row in self.matrix)

    def add_matrices(self, other):
        if self.rows == other.rows and self.collum == other.collum:
            for row_1, row_2 in zip(self.matrix, other.matrix):
                row = []
                for collum_1, collum_2 in zip(row_1, row_2):
                    row.append(collum_1 + collum_2)
                self.result.append(row)
            return Matrix(self.result)

    def multiply_scalar(self, constant):
        for row in self.matrix:
            self.result.append([collum * constant for collum in row])
        return Matrix(self.result)

    def multiply_matrices(self, other):
        if self.collum == other.rows:
            for index_1 in range(int(self.rows)):
                row_1 = []
                for index_2 in range(int(other.collum)):
                    row_2 = []
                    for num_1, num_2 in zip(self.matrix[index_1], other.matrix):
                        row_2.append(num_1 * num_2[index_2])
                    row_1.append(sum(row_2))
                self.result.append(row_1)
            return Matrix(self.result)

    def transpose_matrix(self, target):
        if target == 'main':
            for collum in range(int(self.collum)):
                self.result.append([row[collum] for row in self.matrix])
        elif target == 'side':
            for collum in range(int(self.collum)):
                self.result.append([row[::-1][collum] for row in self.matrix[::-1]])
        elif target == 'vertical':
            for row in self.matrix:
                self.result.append(row[::-1])
        else:
            for row in self.matrix[::-1]:
                self.result.append(row)
        return Matrix(self.result)

    def calculate_determinant(self, matrix=None):
        matrix = self.matrix if matrix is None else matrix
        if len(matrix) == len(matrix[0]):
            if len(matrix) == 1:
                return matrix[0][0]
            elif len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            else:
                result, main, sub = [], matrix[0], matrix[1:]
                for i in range(len(main)):
                    vector = main[i] if i % 2 == 0 else -main[i]
                    minor = [[k for j, k in enumerate(row) if j != i] for row in sub]
                    result.append(vector * self.calculate_determinant(minor))
                return sum(result)
        else:
            return 'Matrix is not square'

    def calculate_inverse(self):
        determinant = self.calculate_determinant(self.matrix)
        if determinant == 0:
            return "This matrix doesn't have an inverse."
        else:
            for r_i, row in enumerate(self.matrix):
                co_row = []
                for c_i, num in enumerate(row):
                    sub = [row for row in self.matrix if self.matrix.index(row) != r_i]
                    minor = [row[:c_i] + row[c_i + 1:] for row in sub]
                    co_row.append(self.calculate_determinant(minor) * (-1) ** (r_i + c_i))
                self.result.append(co_row)
            return Matrix(self.result).transpose_matrix('main').multiply_scalar(1 / determinant)


class Program:

    @staticmethod
    def start_menu():
        print('1. Add matrices')
        print('2. Multiply matrix by a constant')
        print('3. Multiply matrices')
        print('4. Transpose matrix')
        print('5. Calculate a determinant')
        print('6. Inverse matrix')
        print('0. Exit')
        choice = input('Your choice: ')
        if not choice or choice not in ['1', '2', '3', '4', '5', '6', '0']:
            print('Invalid input')
            Program.start_menu()
        if choice == '0':
            exit()
        return choice

    @staticmethod
    def main():
        choice, result = Program.start_menu(), None
        if choice in ['2', '5', '6']:
            first = Matrix()
            first.create()
            if choice == '2':
                constant = int(input('Enter constant: '))
                result = first.multiply_scalar(constant)
            elif choice == '6':
                result = first.calculate_inverse()
            else:
                result = first.calculate_determinant()
        elif choice == '4':
            choice = Program.transpose_menu()
            first = Matrix()
            first.create()
            result = first.transpose_matrix(choice)
        else:
            first, second = Matrix(), Matrix()
            first.create('first')
            second.create('second')
            if choice == '1':
                result = first.add_matrices(second)
            else:
                result = first.multiply_matrices(second)
        if result:
            if not isinstance(result, Matrix):
                print(result, end='\n\n')
            else:
                print('The result is:', result, sep='\n', end='\n\n')
            Program.main()
        else:
            print('The operation cannot be performed.', end='\n\n')
            Program.main()

    @staticmethod
    def transpose_menu():
        print('1. Main diagonal')
        print('2. Side diagonal')
        print('3. Vertical line')
        print('4. Horizontal line')
        choice, result = input('Your choice: '), None
        if not choice or choice not in ['1', '2', '3', '4']:
            print('Invalid input')
            Program.transpose_menu()
        else:
            target = {'1': 'main', '2': 'side', '3': 'vertical', '4': 'horizontal'}
            return target[choice]


if __name__ == '__main__':
    MATRIX_PROCESSOR = Program()
    MATRIX_PROCESSOR.main()
