import sys
import numpy as np
from numpy import linalg
import csv
import pandas as pd
import matplotlib.pyplot as plt


def main(file):

    reader = pd.read_csv("toy.csv")
    plt.plot(reader['year'], reader['days'])
    plt.xlabel('Year')
    plt.ylabel('Days')
    plt.savefig('plot.jpg')

    cur = list(list())
    x = reader["year"]
    for row in x:
        val = [1, row]
        cur.append(val)
    X = np.array(cur)
    print('Q3a: ')
    print(X)

    y = reader['days']
    Y = np.array([y])
    print('Q3b: ')
    print(Y)

    Z = np.dot(X.T, X)
    print('Q3c: ')
    print(Z)

    I = np.linalg.inv(Z)
    print("Q3d: ")
    print(I)

    PI = np.dot(I, X.T)
    print('Q3e: ')
    print(PI)

    hat_beta = np.dot(PI, Y.T).T
    print('Q3f: ')
    print(hat_beta)

    B = hat_beta.T
    Y_test = B[0] + B[1] * 2021
    print('Q4: ' + str(Y_test[0]))

    print('Q5a: <')
    print('Q5b: the ice day is decreasing after a year')

    X_star = -B[0] / B[1]
    print('Q6a: ' + str(X_star[0]))
    print('Q6b: the ice day continue to decrease, suggesting that there will be no ice days in future.')

if __name__ == "__main__":
    x = sys.argv[0]
    main(x)
