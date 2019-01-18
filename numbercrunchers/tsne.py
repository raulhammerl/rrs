from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patheffects as PathEffects
from mpl_toolkits.mplot3d import Axes3D

import time

sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}
from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['PF DinDisplay Pro']
yellow ='#FEDE3D'

def run_tsne(X, dimension, perplex):
    t0 = time.time()
    tsne = TSNE(n_components=dimension, verbose=1, perplexity=perplex, n_iter=10000) #, init='pca')
    X_tsne = tsne.fit_transform(X)
    t1 = time.time() - t0
    print("[tsne] embedding in {}".format(t1))
    return X_tsne

def scatter_tsne_3d(X, colors, perplex):
    # choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", colors.shape[0],))

    # create a scatter plot.
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(X[:,0], X[:,1], X[:,2], lw=0,
                    c=colors, cmap='tab20b', alpha=0.30)
    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    # plt.zlim(-50, 50)
    # ax.axis('off')
    ax.axis('tight')
    ax.view_init(22, 50)
    ax.set_title('tSNE with perplexity: {}'.format(perplex), fontsize=18)

    # file_name = "tSNE" + str(perplex) + "-" + str(dimension) +"D" + ".png"
    # plt.savefig(file_name)
    # print("saving plot to {}".format(file_name))
    plt.show()

def scatter_tsne(data, target, perplex):
    palette = sns.color_palette('deep', np.unique(target).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
    f = plt.figure(figsize=(10, 10))
    ax = plt.subplot(aspect='equal')
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    plt.axis('off')

    ## add the labels for each group
    for i in target.unique():
        # Position of each label.
        xtext, ytext = np.mean(data[target==i], axis=0)
        text = target.get(i)
        plt.annotate(text, (xtext, ytext),
            horizontalalignment='center',
                     verticalalignment='center',
                     size=22, weight='bold',
                     color='white',
                     backgroundcolor=palette[i])
                     #color=palette[i]

    plt.xlim(-50, 50)
    plt.ylim(-50, 50)
    ax.axis('off')
    ax.axis('tight')
    ax.set_title('t-SNE with perplexity: {}'.format(perplex), fontsize=20)

    # plt.show()
    file_name = "tSNE" + str(perplex) + ".png"
    plt.savefig(file_name)
    print("saving plot to {}".format(file_name))



def tsne_perplexity_test(X, y, dimension):
    # make step size a 10th of number of data points
    step_size = X.shape[0]/10

    # run t sne with multiple complexity values
    for perplexity in range(10, X.shape[0], int(step_size)): #X.shape[0] = number of n perplexity needn't be higher
        X_tsne = run_tsne(X, dimension, perplexity)
        scatter_tsne(X_tsne, y, perplexity)
