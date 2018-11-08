from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patheffects as PathEffects

from mpl_toolkits.mplot3d import Axes3D



def run_tsne(X, dimension, perplex):
    # t0 = time.time()
    tsne = TSNE(n_components=dimension, verbose=1, perplexity=perplex, n_iter=10000) #, init='pca')
    X_tsne = tsne.fit_transform(X)
    # plot_embedding(X_tsne,
    #                 y,
    #                "t-SNE embedding of the digits (time %.2fs)" %
    #                (time.time() - t0))
    # plt.show()
    return X_tsne


def scatter_3d_tsne(X, colors, perplex):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", colors.shape[0],))

    # We create a scatter plot.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(X[:,0], X[:,1], X[:,2], lw=0, #lw s
                    c=colors, cmap='viridis')   #palette)
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    # plt.zlim(-50, 50)
    # ax.axis('off')
    ax.axis('tight') #tight
    ax.view_init(60, 35)
    ax.set_title('T-Sne with perplexity: {}'.format(perplex))
    plt.show()

def scatter_tsne(X, colors, perplex):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", colors.shape[0],))

    # We create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(X[:,0], X[:,1], lw=0, s=40,
                    c=colors, cmap='viridis')   #palette)
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    ax.axis('off')
    ax.axis('tight') #tight
    ax.set_title('T-Sne with perplexity: {}'.format(perplex))

    # We add the labels for each digit.
    txts = []
    for i in range(10):
        # Position of each label.
        xtext, ytext = np.median(X[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)
    # plt.show()
    file_name = "tSNE" + str(perplex) + ".png"
    plt.savefig(file_name)
    print("saving plot to {}".format(file_name))
    return f, ax, sc, txts


def tsne_validation(X, y, dimension):
    # run t sne with multiple complexity values
    for i in range(10, 100, 10): #X.shape[0],
        X_tsne = run_tsne(X, dimension, i)
        scatter_tsne(X_tsne, y, i)
