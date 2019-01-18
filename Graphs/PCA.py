from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['PF DinDisplay Pro']
rcParams.update({'font.size': 20})
yellow ='#FEDE3D'

dim = 4
rng = np.random.RandomState(1)
X = np.dot(rng.rand(dim, dim), rng.randn(dim, 200)).T

def scatter_data():
    plt.scatter(X[:, 0], X[:, 1])
    plt.axis('equal');
    plt.show()


def draw_vector(pca, v0, v1, ax=None):
    ax = ax or plt.gca()
    arrowprops=dict(arrowstyle='->',
                    linewidth=2,
                    color = 'r',
                    shrinkA=0, shrinkB=0)
    ax.annotate('', v1, v0, arrowprops=arrowprops)

def pc_vecotrs():
    # plot data
    plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
    pca = PCA(n_components=2)
    pca.fit(X)
    for length, vector in zip(pca.explained_variance_, pca.components_):
        v = vector * 3 * np.sqrt(length)
        draw_vector(pca, pca.mean_, pca.mean_ + v)
    plt.axis('equal');
    plt.show()


def explained_variance_bar_diagram():
    pca = PCA(n_components=3)
    pca.fit(X)
    objects = ["pc1", "pc2", "pc3"]
    y_pos = np.arange(len(objects))
    expl_var = pca.explained_variance_ratio_
    expl_var = expl_var * 100
    print(expl_var)
    plt.ylabel('Erklärtes Varianzverhältnis', fontsize=18)
    plt.title('Hauptkomponenten', fontsize=18)
    plt.xticks(y_pos, objects, fontsize=18)
    # plt.yticks(0,100,20)

    # plt.axis([None, None, 0, 100])
    bar = plt.bar(y_pos, expl_var, width = 0.8 ,align='center', alpha=1, color=yellow)

    for rect in bar:
         height = rect.get_height()
         plt.text(rect.get_x() + rect.get_width()/2.0, height, ("{:.2f}%").format(height), ha='center', va='bottom')


    plt.show()


explained_variance_bar_diagram()
# pc_vecotrs()
