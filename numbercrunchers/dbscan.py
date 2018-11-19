from sklearn.cluster import DBSCAN
import numpy as np

def dbscan(X, pca_2d):
    # DBSCAN(algorithm='auto', eps=3, leaf_size=30, metric='euclidean',
    #     metric_params=None, min_samples=2, n_jobs=None, p=None)

    clustering = DBSCAN(min_samples=2).fit(X)
    print(clustering)
    print(clustering.labels_)

    for i in range(0, pca_2d.shape[0]):
        if clustering.labels_[i] == 0:
            c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r',marker='+')
        elif clustering.labels_[i] == 1:
            c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',marker='o')
        elif clustering.labels_[i] == -1:
            c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b', marker='*')
        # plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2', 'Noise'])
    plt.title('DBSCAN finds clusters and noise')
    plt.show()
