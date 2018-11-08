from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['ArcherPro-Semibold']


def run_aggloreative_clustering(X, n, y):
    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='ward')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='rainbow')
    plt.title('linkage criterion: ward')

    file_name = "agglomerative" + '_ward_' + ".png"
    plt.savefig(file_name)


    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='average')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='rainbow')
    plt.title('linkage criterion: average')

    file_name = "agglomerative" + '_average_' + ".png"
    plt.savefig(file_name)

    cluster = AgglomerativeClustering(n_clusters=n, affinity='euclidean', linkage='complete')
    cluster.fit_predict(X)
    print(cluster.labels_)
    plt.scatter(X[:,0],X[:,1], c=cluster.labels_, lw=0.1 ,cmap='rainbow')
    plt.title('linkage criterion: complete')

    file_name = "agglomerative" + '_complete_' + ".png"
    plt.savefig(file_name)


    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='plasma') #, alpha=0.8
    plt.title('actual instances classified by show')
    file_name = "actual" + '_aggl_' + ".png"
    plt.savefig(file_name)

    #
    # f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    # #plot results
    # ax1.scatter(X[:, 0], X[:, 1], c=cluster.labels_, s=50, alpha=0.8, cmap='rainbow')
    # ax1.set_title('agglomerative predicted clusters')
    #
    # # Add the text label
    # # for i in range(len(y)):
    # #     plt.text(X[i, 0], X[i, 1], y[i], va="top", family="monospace")
    # ax2.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='plasma') #, alpha=0.8
    # ax2.set_title('actual instances classified by show')
    # plt.show()
