import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler


from sklearn.cluster import DBSCAN


import PCA
import kmeans

class NumberCruncher():

    def __init__(self, directory):
        self.directory = directory
        self._load_df('df')


    def _load_df(self, name):
        df_file = os.path.join(self.directory, 'Data', 'Database', name +'.pkl')
        self.df = pd.read_pickle(df_file)
        print(self.df)

    def _run_normalizer(self):
        scaler = Normalizer().fit(X)
        normalizedX = scaler.transform(X)
        return normalizedX

    def _run_scaler(self):
        # Get column names first
        names = self.df.columns
        # Create the Scaler object
        scaler = StandardScaler()
        # Fit your data on the scaler object
        data_scaled = scaler.fit_transform(self.df)
        self.df = pd.DataFrame(data_scaled, columns=names)


    def _drop_columns_containing(self, cue):
        to_drop = [c for c in self.df.columns if(cue in c)]
        # print("dropping: {}".format(to_drop))
        self.df.drop(to_drop, axis=1, inplace=True)

    def _select_columns_containing(self, cue):
        to_select = [c for c in self.df.columns if(cue in c)]
        self.df.loc[:, to_select]

    def _get_nearest_neigbours(self, df, df_target, n):
        ## Instantiate the model with n neighbors.
        X_train, X_test, y_train, y_test = train_test_split(df, df_target, test_size=0.3) # 70% training and 30% tes

        knn = KNeighborsClassifier(n_neighbors=n)
        ## Fit the model on the training data.
        knn.fit(X_train, y_train)
        ## See how the model performs on the test data.
        knn.score(X_test, y_test)

        #Predict the response for test dataset
        y_pred = knn.predict(X_test)

        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:", metrics.accuracy_score(y_test, y_pred))


    def _write_to_excel(self, pages):
        output = os.path.join(self.directory, 'Data', 'Database', 'output.xlsx')
        writer = pd.ExcelWriter(output)

        i = 0
        for page in pages:
            page.to_excel(writer,('Sheet'+ str(i)))
            i += 1
        writer.save()
    def _write_to_csv(self, directory):
        file_name = os.path.join(self.directory, 'Data', 'Database', 'pandasDF.csv')
        self.df.to_csv(file_name, encoding='utf-8', index=False)


    def _clean_df(self):
        #fixing messy column names
        #could also be done by calling columns with: df['name_of_column']
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace('.', '_').str.replace('(', '').str.replace(')', '')

        # give boolean value to minor and major chords
        self.df.tonal_chords_scale = self.df.tonal_chords_scale.replace({"minor": "0", "major": "1"})
        self.df.tonal_key_scale = self.df.tonal_key_scale.replace({"minor": "0", "major": "1"})

        # one hot encode scale key columns
        cols_to_transform = [ 'tonal_chords_key', 'tonal_key_key']
        self.df = pd.get_dummies(self.df, columns = cols_to_transform)

        # get metadata columns
        file_name_column = self.df.metadata_tags_file_name
        show_id_column = self.df.metadata_tags_album_0
        recording_id_column = self.df.metadata_tags_tracknumber_0
        channel_id = self.df.metadata_tags_artist_0
        meta_df = pd.concat([file_name_column, show_id_column, recording_id_column, channel_id], axis=1)
        meta_df.columns = ['file_name',  'show_id', 'recording_id', 'channel_id']

        # drop metadata values
        # to_drop = [c for c in df.columns if c.lower()[:8] == 'metadata']
        # print(to_drop)
        # df = df.drop(to_drop, axis=1)
        self._drop_columns_containing("metadata")

        self.df = pd.concat([meta_df, self.df], axis=1)
        print (self.df)
        return self.df

def dbscan(X, pca_2d):
    # DBSCAN(algorithm='auto', eps=3, leaf_size=30, metric='euclidean',
    #     metric_params=None, min_samples=2, n_jobs=None, p=None)

    clustering = DBSCAN(eps=3, min_samples=2).fit(X)
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
    plt.title('DBSCAN finds 2 clusters and noise')
    plt.show()



def main(self):
    # self._clean_df()
    y = self.df ['channel_id']
    self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1, inplace=True)

    self.df = self.df.dropna(axis=1, how='any')

    self._drop_columns_containing("beats_position")
    self._drop_columns_containing("mfcc")
    self._drop_columns_containing("dmean2")
    self._drop_columns_containing("dmean")
    self._drop_columns_containing("dvar")
    self._drop_columns_containing("dvar2")
    self._drop_columns_containing("max")
    self._drop_columns_containing("min")
    self._drop_columns_containing("median")

    self._run_scaler()
    # pca = PCA.run_pca(self.df, 15)
    kpca = PCA.run_kpca(self.df, 15)
    pca_2d = PCA.run_pca(self.df, 2)
    # PCA.print_cumsum_trend(pca)
    # kmeans.calculate_k_means(pca, 6, y)

    # PCA.print_cumsum_trend_kpca(pca)
    # PCA.print_cumsum_trends_vs(kpca, pca)
    # X_tsne = PCA.run_tsne(kpca, y, 2)
    dbscan(kpca, pca_2d)
    # PCA.print_heatmap(self.df, 20, 400)


if __name__ == "__main__":
    # directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder'
    directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/Database'
    nc = NumberCruncher(directory)
    main(nc)
