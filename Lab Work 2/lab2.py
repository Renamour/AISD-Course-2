import numpy as np
from numpy import linalg

mx = int(input('Необходимо ввести размерность квадратной матрицы (> 1 и < 15)'))

while (mx < 1) or (mx > 15):
    mx = int(input("Необходимо ввести указанные числа"))
sizee = np.random.randint(5, size=(mx, mx))

print("Итоговая матрица:\n", sizee)
rang = np.linalg.matrix_rank(sizee)
print("\nРанг матрицы:", rang)
sign = int(input('Необходимо ввести количество знаков после запятой:'))
sign = 0.1 ** sign
n = 1
factorial = 1
summ = 0
fg = 0
fract = 1
while abs(fract) > sign:
    fg += summ
    summ += (np.linalg.det(linalg.matrix_power(sizee, 4 * n - 1))) / factorial
    n += 1
    factorial = factorial * (4*n - 1) * (2*n)
    fract = abs(fg-summ)
    fg = 0
    print(n-1, ':', summ, ' ', fract)
print('Сумма знакопеременного ряда:', summ)