from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['Verlag']




def calculate_k_means(X, n, y):
    kmeans = KMeans(n_clusters = n)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_

    fig = plt.figure(figsize=(10, 10))
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    #plot results
    ax1.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, alpha=0.8, cmap='tab20c')
    ax1.scatter(centers[:, 0], centers[:, 1], c='black', s=120, alpha=0.3)
    ax1.set_title('K-Means predicted clusters')

    # Add the text label
    # for i in range(len(y)):
    #     plt.text(X[i, 0], X[i, 1], y[i], va="top", family="monospace")
    ax2.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='tab20b') #, alpha=0.8
    ax2.set_title('actual instances classified by channel')
    plt.show()

    # calculate adjusted rand score
    labels_true = y.values
    # labels_true = labels_true -1  # not necessary
    labels_pred = y_kmeans
    score = adjusted_rand_score(labels_true, labels_pred)
    print("[k-Means] Accuracy: {}".format(score))


def calculate_k_means_3d(X, n, y):
    kmeans = KMeans(n_clusters = n)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_

    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    #plot results
    ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=y_kmeans, alpha=1, cmap='viridis')
    ax1.scatter(centers[:, 0], centers[:, 1], c='black', alpha=0.5)
    ax1.set_title('K-Means predicted clusters', fontsize=18)

    # Add the text label
    # for i in range(len(y)):
    #     plt.text(X[i, 0], X[i, 1], y[i], va="top", family="monospace")
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap='plasma') #, alpha=0.8
    ax2.set_title('actual instances classified by show', fontsize=18)
    plt.show()

    # calculate adjusted rand score
    labels_true = y.values
    # labels_true = labels_true -1  # not necessary
    labels_pred = y_kmeans
    score = adjusted_rand_score(labels_true, labels_pred)
    print("[k-Means3D] accuracy: {}".format(score))
