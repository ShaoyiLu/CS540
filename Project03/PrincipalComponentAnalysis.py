from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    x = np.load(filename)
    mean = np.mean(x, axis=0)
    x = x - mean
    return x

def get_covariance(dataset):
    x = np.dot(np.transpose(dataset), dataset)
    x = x / (len(dataset) - 1)
    return x

def get_eig(S, m):
    Lambda, U = eigh(S, subset_by_index=[1024-m, 1023])
    U = np.fliplr(U)
    Lambda = np.sort(Lambda)[::-1]
    Lambda = np.diag(Lambda)
    return Lambda, U

def get_eig_prop(S, prop):
    Lambda, U = eigh(S)
    x = sum(Lambda)*prop
    Lambda, U = eigh(S, subset_by_value=[x, np.inf])
    U = np.fliplr(U)
    Lambda = np.sort(Lambda)[::-1]
    Lambda = np.diag(Lambda)
    return Lambda, U


def project_image(image, U):
    projection = np.zeros(len(image))
    for i in range(len(U[0])):
        projection += np.dot(U[:, i], image)*(U[:, i])
    return projection

def display_image(orig, proj):
    orig = orig.reshape(32, 32)
    orig = np.transpose(orig)
    proj = proj.reshape(32, 32)
    proj = np.transpose(proj)
    fig, ax = plt.subplots(1, 2)
    ax[0].set_title('Original')
    ax[1].set_title('Projection')
    colorbarOrig = ax[0].imshow(orig, aspect='equal')
    colorbarProj = ax[1].imshow(proj, aspect='equal')
    fig.colorbar(colorbarOrig, ax=ax[0])
    fig.colorbar(colorbarProj, ax=ax[1])
    plt.show()

