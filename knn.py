from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report

import matplotlib.pyplot as plt

def _get_nearest_neigbours(X, y, n):
    # dist = DistanceMetric.get_metric('euclidean')

    ## Instantiate the model with n neighbors.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% tes

    knn = KNeighborsClassifier(n_neighbors=n, p=2)
    ## Fit the model on the training data.
    knn.fit(X_train, y_train)
    ## See how the model performs on the test data.
    knn.score(X_test, y_test)

    #Predict the response for test dataset
    y_pred = knn.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", accuracy_score(y_test, y_pred))
    # Print out classification report and confusion matrix
    print("\n\n")
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
