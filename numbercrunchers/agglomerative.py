from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['Verlag']

def compare_aggloreative_clustering(X, n, y):
    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='ward')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.figure(figsize=(10, 10))
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='tab20c')
    plt.title('linkage criterion: ward', fontsize=18)
    file_name = "agglomerative" + '_ward_' + ".png"
    plt.savefig(file_name)


    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.figure(figsize=(10, 10))
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='tab20c')
    plt.title('linkage criterion: average', fontsize=18)
    file_name = "agglomerative" + '_average_' + ".png"
    plt.savefig(file_name)

    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='complete')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.figure(figsize=(10, 10))
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='tab20c')
    plt.title('linkage criterion: complete', fontsize=18)
    file_name = "agglomerative" + '_complete_' + ".png"
    plt.savefig(file_name)

    plt.figure(figsize=(10, 10))
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='tab20b') #, alpha=0.8
    plt.title('actual instances classified by show', fontsize=18)
    file_name = "actual" + '_aggl_' + ".png"
    print("saving: ", file_name)
    plt.savefig(file_name)




def run_aggloreative_clustering(X, y, n):
    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    # print(cluster.labels_)
    # plt.figure(figsize=(12, 9))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    #plot results
    ax1.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='tab20c')
    ax1.set_title('agglomerative predicted clusters', fontsize=18)

    # plot actual groups
    ax2.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='tab20b') #, alpha=0.8
    ax2.set_title('actual instances classified by channel', fontsize=18)
    plt.show()

    print(y.unique())
