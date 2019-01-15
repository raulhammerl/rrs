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

yellow ='#FEDE3D'

def print_cumsum_trend(X, dimension, ker='poly'):
    x_kpca = KernelPCA(n_components = dimension, kernel=ker, gamma=15).fit_transform(X)
    explained_variance = np.var(x_kpca, axis=0)
    print(explained_variance)
    explained_variance_ratio = explained_variance / np.sum(explained_variance)
    print(explained_variance_ratio)
    print(np.cumsum(explained_variance_ratio))
    plt.plot(np.cumsum(explained_variance_ratio), color = yellow)
    plt.xlabel('Komponenten')
    plt.ylabel('gesamte erklärte Varianz')
    plt.grid(b=None, which='major', axis='both', linestyle='dotted')
    plt.show()


def print_cumsum_trend_vs(X):
    dimension = 100
    kpca = KernelPCA(n_components = dimension, kernel="poly", gamma=15).fit_transform(X)
    pca = PCA(n_components = dimension).fit_transform(X)

    explained_variance = np.var(kpca, axis=0)
    print(explained_variance)
    explained_variance_ratio = explained_variance / np.sum(explained_variance)
    print(explained_variance_ratio)
    print(np.cumsum(explained_variance_ratio))
    kpca_plot = np.cumsum(explained_variance_ratio)
    plt.xlabel('Komponenten')
    plt.ylabel('gesamte erklärte Varianz')
    plt.grid(b=None, which='major', axis='both', linestyle='dotted')


    red_patch = mpatches.Patch(color='red', label='polynomial KPCA')
    green_patch = mpatches.Patch(color='green', label='PCA')
    plt.legend(handles=[red_patch, green_patch])

    pca_explained_variance = np.var(pca, axis=0)
    pca_explained_variance_ratio = pca_explained_variance / np.sum(pca_explained_variance)
    pca_plot = np.cumsum(pca_explained_variance_ratio)
    plt.plot(kpca_plot, 'r', pca_plot, 'g')
    plt.show()



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

def select_most_important_features(data, n_comp, n_features):
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
    # print(data)
    dictionary = dict(zip(vif_ind, vif_values))
    sorted_d = sorted(dictionary.items(), key=lambda kv: kv[1])

    # print("pca_data", pca_data)
    # print("pca_inv_data", pca_inv_data)
    # print("mean", mean)
    # print("mean abs", mean_abs)
    # print(vif_values)
    # print("z_d", z_data)
    # print(vif_ind)
    # print(dictionary)
    # print(sorted_d)

    vif_ind = [i[0] for i in sorted_d]
    vif_features_names = data.iloc[:,vif_ind]
    # print(vif_features_names.columns.values)
    return vif_features_names.columns.values

def get_vip_feature_count(data, n_comp, n_features, runs=1000):
    a = []
    for i in range(runs):
        x = select_most_important_features(data, n_comp, n_features)
        a.extend(x)
    unique, counts = np.unique(a, return_counts=True)
    d = dict(zip(unique, counts))
    print("lenght", len(d))

    sorted_d = sorted(d.items(), reverse=True, key=lambda x: x[1])

    for elem in sorted_d:
        print(elem[0] , " ::" , elem[1] )
    # sorted_d = [(k,v) for k,v in d.items()]
    # items = [(k, v) for k, v in d.items()]
    # items.sort()
    # items.reverse() # so largest is first
    # sorted_d = [(k, v) for k, v in items]
    # print(sorted_d)
    # pretty(sorted_d)
    return d

def get_clostest_shows(df, needle, dimension=100):
    neigh = get_neigh()
    show_ids = odf['show_id'].iloc(neigh)
    show_ids.groupby('show_id')['ID'].nunique()
    # unique, counts = np.unique(show_ids, return_counts=True)
    # d = dict(zip(unique, counts))
    sorted_d = [(k,v) for k,v in d.items()]


def pretty(d, indent=0):
   for key, value in d:
      print('\t' * indent + str(key) + " : " + str(value))
      # if isinstance(value, dict):
      #    pretty(value, indent+1)
      # else:
      #    print('\t' * (indent+1) + str(value))


def draw_vector(v0, v1, ax=None):
    ax = ax or plt.gca()
    arrowprops=dict(arrowstyle='->',
                    linewidth=2,
                    shrinkA=0, shrinkB=0)
    ax.annotate('', v1, v0, arrowprops=arrowprops)


def print_heatmap(data, n_comp, xlim):
    pca_trafo = PCA(n_components=n_comp)
    z_scaler = StandardScaler()
    z_data = z_scaler.fit_transform(data)

    pca_data = pca_trafo.fit_transform(z_data)
    pca_inv_data = pca_trafo.inverse_transform(np.eye(n_comp))

    fig = plt.figure(figsize=(10, 6.5))
    sns.heatmap(pca_trafo.inverse_transform(np.eye(n_comp)), cmap="hot", cbar=False)
    plt.ylabel('principal component', fontsize=20)
    plt.xlabel('original feature index', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=12)

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
