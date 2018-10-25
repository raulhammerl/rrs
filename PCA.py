import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as PathEffects
import time

from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from matplotlib import offsetbox

# def print_cumsum_trend(pca):
#     plt.plot(np.cumsum(pca.explained_variance_ratio_))
#     plt.xlabel('number of components')
#     plt.ylabel('cumulative explained variance');
#
#     plt.grid(b=None, which='major', axis='both', linestyle='dotted')
#     plt.show()

def print_cumsum_trend(kpca):
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


def print_cumsum_trends_vs(kpca, pca):
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


def run_tsne(X, y, dimension):
    t0 = time.time()
    tsne = TSNE(n_components=dimension, verbose=1, perplexity=50, n_iter=3000) # init='pca'
    X_tsne = tsne.fit_transform(X)
    # plot_embedding(X_tsne,
    #                 y,
    #                "t-SNE embedding of the digits (time %.2fs)" %
    #                (time.time() - t0))
    # plt.show()
    scatter_tsne(X_tsne, y)
    return X_tsne
    # plt.savefig('images/digits_tsne-generated.png', dpi=120)


def plot_embedding(X, y, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure()
    ax = plt.subplot(111)
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(y[i]),
                 color=plt.cm.Set1(y[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})
    #
    # if hasattr(offsetbox, 'AnnotationBbox'):
    #     # only print thumbnails with matplotlib > 1.0
    #     shown_images = np.array([[1., 1.]])  # just something big
    #     for i in range(X.shape[0]):
    #         dist = np.sum((X[i] - shown_images) ** 2, 1)
    #         if np.min(dist) < 4e-3:
    #             # don't show points that are too close
    #             continue
    #         shown_images = np.r_[shown_images, [X[i]]]
    #         imagebox = offsetbox.AnnotationBbox(
    #             offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
    #             X[i])
    #         ax.add_artist(imagebox)
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)

def scatter_tsne(x, colors):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", 10))

    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40,
                    c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis('off')
    ax.axis('tight')

    # We add the labels for each digit.
    txts = []
    for i in range(10):
        # Position of each label.
        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)
    plt.show()
    return f, ax, sc, txts



def print_cumsums():
    print(pca.components_)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_.cumsum())


def normalize_data():
    pass

def run_pca(X, dimension):
    pca = PCA(n_components = dimension).fit(X)
    pca_df = pca.transform(X)
    return pca_df

def run_kpca(X, dimension):
    kpca = KernelPCA(n_components = dimension, kernel="cosine", gamma=15)
    X_kpca = kpca.fit_transform(X)
    return X_kpca

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
    mean = pca_inv_data.mean(axis=0)
    features_selected = np.argwhere((mean > 0.01) | (mean < -0.01))
    print(features_selected.size)
    # print(features_selected)
    # print(features_selected.descriptor)
    # print(data.iloc[:features_selected])


    ## filter only high amplitude 'mean'
    plt.plot(pca_inv_data.mean(axis=0), '--o', label = 'mean')
    plt.plot(np.square(pca_inv_data.std(axis=0)), '--o', label = 'variance')
    plt.legend(loc='lower right')
    plt.ylabel('feature contribution', fontsize=20);
    plt.xlabel('feature index', fontsize=20);
    plt.tick_params(axis='both', which='major', labelsize=14);
    plt.tick_params(axis='both', which='minor', labelsize=12);
    plt.xlim([0, xlim])
    plt.legend(loc='lower left', fontsize=18)

    plt.show()
