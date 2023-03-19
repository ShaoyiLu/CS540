import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy


def load_data(filepath):
    dict = list()
    with open(filepath, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        x = len(open(filepath, encoding='utf=8').readlines())
        for row in reader:
            dict.append(row)
            i = 0
            if (i == x - 1):
                break
            dict[i]['Attack'] = int(row['Attack'])
            dict[i]['Sp. Atk'] = int(row['Sp. Atk'])
            dict[i]['Speed'] = int(row['Speed'])
            dict[i]['Defense'] = int(row['Defense'])
            dict[i]['Sp. Def'] = int(row['Sp. Def'])
            dict[i]['HP'] = int(row['HP'])
            i += 1
    return dict


def calc_features(row):
    x = np.zeros(shape=(6, 0))
    dict = np.append(x, list((int(row['Attack']), int(row['Sp. Atk']), int(row['Speed']), int(row['Defense']),
                              int(row['Sp. Def']), int(row['HP']))))

    return dict.astype(np.int64)


def hac(features):
    n = len(features)
    matrix = np.zeros([n, n])
    final = np.zeros([0, 4])
    datum = dict()

    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                matrix[i][j] = np.linalg.norm(features[i] - features[j])

    for name in range(0, n):
        datum[name] = [name]

    index = n
    for x in range(0, n - 1):
        min = float('inf')

        a = 0
        b = 0
        for i in datum:
            for j in datum:
                if i == j:
                    continue;

                max = float('-inf')
                cluster1 = datum[i]
                cluster2 = datum[j]

                for k in cluster1:
                    for l in cluster2:
                        if max < matrix[k][l]:
                            max = matrix[k][l]

                if min > max:
                    min = max
                    a = i
                    b = j
                elif max == min:
                    if a > i:
                        a = i
                        b = j
                    elif a == i:
                        if b > j:
                            b = j

        datum[index] = datum[a] + datum[b]
        del datum[b]
        del datum[a]
        c = list((a, b, min, len(datum[index])))
        final = np.vstack(list((final, c)))
        index += 1
    return final


def imshow_hac(Z):
    plt.figure()
    hierarchy.dendrogram(Z)
    plt.show()


if __name__ == "__main__":
    n = 20
    z = hac([calc_features(row) for row in load_data("Pokemon.csv")][:n])
    imshow_hac(z)