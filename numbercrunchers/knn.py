from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report

from sklearn.metrics import roc_curve

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from matplotlib import rcParams
rcParams['font.family'] = ['sans-serif']
rcParams['font.sans-serif'] = ['Verlag']




def _get_nearest_neigbours(X, y, n_neighbors):
    ## Instantiate the model with n neighbors.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% tes

    knn = KNeighborsClassifier(n_neighbors, p=2)
    ## Fit the model on the training data.
    knn.fit(X_train, y_train)
    ## See how the model performs on the test data.
    knn.score(X_test, y_test)

    #Predict the response for test dataset
    y_pred = knn.predict(X_test)

    # get confusion matrix
    pd.crosstab(y_test, y_pred, rownames=['True'], colnames=['Predicted'], margins=True)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy with {} neighbors: {}".format(n_neighbors, accuracy_score(y_test, y_pred)))

    # Print out classification report and confusion matrix
    print(classification_report(y_test, y_pred))
    # plt.plot(classification_report(y_test, y_pred))
    plt.show()
    # neigh = knn.kneighbors([X[5]])
    # neigh.toarray()
    # knn.kneighbors_graph([X, 10])


def _kkn_cross_validation(X, y):
    # creating odd list of K for KNN
    myList = list(range(1,50))

    # subsetting just the odd ones
    neighbors = list(range(1,50,2))

    # empty list that will hold cv scores
    cv_scores = []

    # perform 10-fold cross validation
    for k in neighbors:
        knn = KNeighborsClassifier(n_neighbors=k ,p=2)
        scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())


    # changing to misclassification error
    MSE = [1 - x for x in cv_scores]

    # determining best k
    optimal_k = neighbors[MSE.index(min(MSE))]
    print ("The optimal number of neighbors is {} with an error rate of {}".format(optimal_k, MSE[15]))

    # plot misclassification error vs k
    plt.plot(neighbors, MSE)
    plt.xlabel('Number of Neighbors K')
    plt.ylabel('Misclassification Error')
    plt.show()

    return optimal_k



def _knn_graph(X, y, n_neighbors):
    ## Instantiate the model with n neighbors.
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% tes

    h =  1#.02 # step size in the mesh


    # Create color maps
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

    for weights in ['uniform', 'distance']:
        # we create an instance of Neighbours Classifier and fit the data.
        clf = KNeighborsClassifier(n_neighbors, weights=weights)
        clf.fit(X, y)

        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.figure()
        plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                    edgecolor='k', s=20)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.title("3-Class classification (k = %i, weights = '%s')"
                  % (n_neighbors, weights))

    plt.show()



def draw_roc(X, y, n_neighbors):
    ## Instantiate the model with n neighbors.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% tes

    knn = KNeighborsClassifier(n_neighbors, p=2)
    ## Fit the model on the training data.
    knn.fit(X_train, y_train)

    # print(y)

    # calculate roc curve
    y_pred_proba = knn.predict_proba(X_test)[:,1]
    fpr, tpr, thresholds = roc_curve(y, y_pred_proba)

    plt.plot([0,1],[0,1],'k--')
    plt.plot(fpr,tpr, label='Knn')
    plt.xlabel('fpr')
    plt.ylabel('tpr')
    plt.title('Knn(n_neighbors=7) ROC curve')
    plt.show()



def get_neigh(X, needle, n):
    # get filepath from recording_id and DB
    # get show_name from id and DB
    # print distances

    neighs = []
    neigh = NearestNeighbors(n_neighbors=n+1)
    neigh.fit(X)
    NearestNeighbors(algorithm='auto', leaf_size=30)
    distances, indices = neigh.kneighbors([X[needle]])
    print("\n\n", distances)
    for x in indices:
        for i in x:
            # if i == needle:
            #     continue
            # else:
            #     neighs.extend([int(i)])
            neighs.extend([int(i)])
    X_neighs = X.iloc[nearestn, 0:4]
    # X_neighs.append(distances, axis=1)
    # print(X_neighs)
    return neighs
