import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler


from sklearn.cluster import DBSCAN

import agglomerative as agg
import PCA
import kmeans
import knn
import tsne

class NumberCruncher():

    def __init__(self, directory):
        self.directory = directory
        self._load_df('30-10-alt')


    def _load_df(self, name):
        df_file = os.path.join(self.directory, 'Data', 'Database', name +'.pkl')
        with open(df_file, "rb") as f:
            self.df = pd.read_pickle(f)


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
        return self.df


    def slct_shows_w_x_instances(self, df, n, k):
        df_selected = pd.DataFrame()
        i=0
        shows = []
        for show_id in range(df['show_id'].max()):
            one_show = df[df['show_id'] == show_id]
            one_show = one_show.head(k) # only if equal no of instances
            if len(one_show.index) >= n:
                # print('yees')
                i= i+1
                shows.append(show_id)
                df_selected = df_selected.append(one_show)
        print("shows with over {} instances: {}".format(n, shows))
        print(i)
        # print(df_selected['file_name'])
        return df_selected

    def slct_x_and_y(self):
        y = self.df ['channel_id']
        X = self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1)
        return (X,y)

    def _does_contain_nan(self, df):
        return self.df.isnull().values.any()


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


def _load_df2(df1, directory, name):
    df2_file = os.path.join(directory, 'Data', 'Database', name +'.pkl')
    df2 = pd.read_pickle(df2_file)
    df_concat = df1.append(df2, ignore_index=True)
    print(df_concat.shape)
    return df_concat


def main(self):

    self.df = _load_df2(self.df, directory,'27-10')
    self._clean_df()
    # y = self.df ['channel_id']
    # self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1, inplace=True)

    self._drop_columns_containing("beats_position")
    self._drop_columns_containing("mfcc")
    self._drop_columns_containing("dmean2")
    self._drop_columns_containing("dmean")
    self._drop_columns_containing("dvar")
    self._drop_columns_containing("dvar2")
    self._drop_columns_containing("max")
    self._drop_columns_containing("min")
    self._drop_columns_containing("median")

    self.df = self.slct_shows_w_x_instances(self.df, 10, 10)

    dupes = self.df.duplicated(subset=None, keep='first')
    print('dupes: ', dupes.sum())
    # print(df)

    # show1 = self.df[self.df['show_id'] == 6]
    # show1 = show1.head(10)
    # # print(show1)
    # show2 = self.df[self.df['show_id'] == 8]
    # show2 = show2.head(10)
    # # print(show2)
    # show3 = self.df[self.df['show_id'] == 20]
    # show3 = show3.head(10)
    #
    # self.df = pd.concat([show1, show2], axis=0)
    # print(self.df.shape)

    y = self.df ['show_id']
    self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1, inplace=True)

    self.df = self.df.dropna(axis=1, how='any')
    self.df = self.df.reset_index()
    self._run_scaler()

    X_kpca = PCA.run_kpca(self.df, 15)

    # PCA.print_cumsum_trend(pca)
    # PCA.print_cumsum_trend_kpca(pca)
    # PCA.print_cumsum_trends_vs(kpca, pca)

    perplexity = 20
    X_tsne = tsne.run_tsne(X_kpca, 2, perplexity)
    # tsne.scatter_3d_tsne(X_tsne, y, 20)
    # tsne.tsne_validation(X_kpca, y , 2)


    # kmeans.calculate_k_means(X_kpca, 2, y)
    # kmeans.calculate_k_means_3d(X_tsne, 2, y)
    # dbscan.dbscan(X_tsne, pca_2d)
    # PCA.print_heatmap(self.df, 20, 400)
    #
    agg.run_aggloreative_clustering(X_tsne, 24, y)
    # agg.run_aggloreative_clustering(X_kpca, 24, y)

    # KNN
    # knn._get_nearest_neigbours(X_kpca, y, 8)
    # knn._get_nearest_neigbours(X_tsne, y, 11)

    # knn._kkn_cross_validation(X_kpca,y)
    # knn._kkn_cross_validation(X_tsne,y)

    # knn._knn_graph(X_tsne, y, 5)

if __name__ == "__main__":
    # directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder'
    directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/Database'
    nc = NumberCruncher(directory)
    main(nc)
