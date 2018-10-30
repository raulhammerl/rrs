from sklearn.cluster import DBSCAN
import numpy as np




def dbscan():
    # DBSCAN(algorithm='auto', eps=3, leaf_size=30, metric='euclidean',
    #     metric_params=None, min_samples=2, n_jobs=None, p=None)

    clustering = DBSCAN(eps=3, min_samples=2).fit(X)
    print(clustering.labels_)
    
