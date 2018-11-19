import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler
from matplotlib import offsetbox
import seaborn as sns

def print_cumsum_trend(X, dimension):
    kpca = KernelPCA(n_components = dimension, kernel="cosine", gamma=15).fit(X)
    explained_variance = np.var(kpca, axis=0)
    print(explained_variance)
    explained_variance_ratio = explained_variance / np.sum(explained_variance)
    print(explained_variance_ratio)
    print(np.cumsum(explained_variance_ratio))
    plt.plot(np.cumsum(explained_variance_ratio))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    plt.grid(b=None, which='major', axis='both', linestyle='dotted')
    plt.show()


def print_cumsum_trends_vs(X):
    dimension = 100
    kpca = KernelPCA(n_components = dimension, kernel="cosine", gamma=15).fit(X)
    pca = PCA(n_components = dimension).fit(X)

    explained_variance = np.var(kpca, axis=0)
    print(explained_variance)
    explained_variance_ratio = explained_variance / np.sum(explained_variance)
    print(explained_variance_ratio)
    print(np.cumsum(explained_variance_ratio))
    kpca_plot = np.cumsum(explained_variance_ratio)
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance');
    plt.grid(b=None, which='major', axis='both', linestyle='dotted')


    red_patch = mpatches.Patch(color='red', label='polynomial KPCA')
    green_patch = mpatches.Patch(color='green', label='PCA')
    plt.legend(handles=[red_patch, green_patch])

    pca_explained_variance = np.var(pca, axis=0)
    pca_explained_variance_ratio = pca_explained_variance / np.sum(pca_explained_variance)
    pca_plot = np.cumsum(pca_explained_variance_ratio)
    plt.plot(kpca_plot, 'r', pca_plot, 'g')
    plt.show()



def print_cumsums():
    print(pca.components_)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_.cumsum())


def run_pca(X, dimension):
    t0 = time.time()
    pca = PCA(n_components = dimension).fit(X)
    X_pca = pca.transform(X)
    t1 = time.time() - t0
    print("[PCA] embedding in {}".format(t1))
    return X_pca

def run_kpca(X, dimension):
    t0 = time.time()
    kpca = KernelPCA(n_components = dimension, kernel="cosine", gamma=15)
    X_kpca = kpca.fit_transform(X)
    t1 = time.time() - t0
    print("[kPCA] embedding in {}".format(t1))
    return X_kpca

def select_most_importan_features(data, n_comp, n_features):
    pca_trafo = PCA(n_components=n_comp)
    z_scaler = StandardScaler()
    z_data = z_scaler.fit_transform(data)

    pca_data = pca_trafo.fit_transform(z_data)
    pca_inv_data = pca_trafo.inverse_transform(np.eye(n_comp))

    # get mean of
    mean = pca_inv_data.mean(axis=0)
    # get absolute mean for most significant features
    mean_abs = np.absolute(mean)
    # get n highest values
    vif_ind = np.argpartition(mean_abs, -(n_features))[-(n_features):]
    vif_values = mean[vif_ind]
    vif_features_names = data.iloc[:,vif_ind]

    dictionary = dict(zip(vif_ind, vif_values))

    sorted_d = sorted(dictionary.items(), key=lambda kv: kv[1])
    print(sorted_d)
    vif_ind = [i[0] for i in sorted_d]
    vif_features_names = data.iloc[:,vif_ind]
    print(vif_features_names.columns.values)

    return vif_features_names.columns.values



def print_heatmap(data, n_comp, xlim):
    pca_trafo = PCA(n_components=n_comp)
    z_scaler = StandardScaler()
    z_data = z_scaler.fit_transform(data)

    pca_data = pca_trafo.fit_transform(z_data)
    pca_inv_data = pca_trafo.inverse_transform(np.eye(n_comp))

    fig = plt.figure(figsize=(10, 6.5))
    sns.heatmap(pca_trafo.inverse_transform(np.eye(n_comp)), cmap="hot", cbar=False)
    plt.ylabel('principal component', fontsize=20);
    plt.xlabel('original feature index', fontsize=20);
    plt.tick_params(axis='both', which='major', labelsize=14);
    plt.tick_params(axis='both', which='minor', labelsize=12);

    fig = plt.figure(figsize=(10, 6.5))


    plt.plot(pca_inv_data.mean(axis=0), '--o', label = 'mean')
    plt.plot(np.square(pca_inv_data.std(axis=0)), '--o', label = 'variance')
    plt.legend(loc='lower right')
    plt.ylabel('feature contribution', fontsize=20);
    plt.xlabel('feature index', fontsize=20);
    plt.tick_params(axis='both', which='major', labelsize=14);
    plt.tick_params(axis='both', which='minor', labelsize=12);
    plt.xlim([0, xlim])
    # plt.legend(loc='lower left', fontsize=18)
    plt.show()
