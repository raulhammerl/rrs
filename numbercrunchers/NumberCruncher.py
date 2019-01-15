import pandas as pd
import numpy as np
import os
import time
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

import pycha as pcha
import hdbscan

import Archetype as arch
import agglomerative as agg
import PCA
import kmeans
import knn
import tsne
import DFSelector as slt
import Plotter as plt





class NumberCruncher():

    def __init__(self, directory):
        self.directory = directory
        self._load_df('10-01')


    def _load_df(self, name):
        df_file = os.path.join(self.directory, 'Data', 'Database', name +'.pkl')
        with open(df_file, "rb") as f:
            self.df = pd.read_pickle(f)


    def _run_normalizer(self, X):
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
        # fixing messy column names
        # could also be done by calling columns with: df['name_of_column']
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
        length = self.df.metadata_audio_properties_length
        meta_df = pd.concat([file_name_column, show_id_column, recording_id_column, channel_id, length], axis=1)
        meta_df.columns = ['file_name',  'show_id', 'recording_id', 'channel_id', 'length']

        # drop metadata values
        # to_drop = [c for c in df.columns if c.lower()[:8] == 'metadata']
        # print(to_drop)
        # df = df.drop(to_drop, axis=1)
        self.df = slt.drop_columns_containing(self.df, ["metadata"])

        self.df = pd.concat([meta_df, self.df], axis=1)
        return self.df


    def select_data_and_target(self):
        y = self.df ['channel_id']
        # drop metadata values
        X = self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1)
        return (X,y)


    def run_clusterings_on(self, X, algorithm, args, kwds, select, target):
        for i in X[select].unique():
            data = self.df[self.df[select] == i]
            target = data[target]
            data.drop(['file_name',  'show_id', 'recording_id', 'channel_id', 'length'], axis=1, inplace=True)
            X_kpca = PCA.run_kpca(data, 15)
            X_tsne = tsne.run_tsne(X_kpca, 2, 110)
            self.plot_clusters(X_tsne, algorithm, args, kwds)
            self.plot_real_clusters(X_tsne, target, label='show', title=channel_labels[i])


def _load_df2(df1, directory, name):
    df2_file = os.path.join(directory, 'Data', 'Database', name +'.pkl')
    df2 = pd.read_pickle(df2_file)
    df_concat = df1.append(df2, ignore_index=True)
    print(df_concat.shape)
    return df_concat


def main(self):
    # self.df = _load_df2(self.df, directory,'14-11')
    self._clean_df()
    d,h,m,s = slt.get_total_recording_time(self.df)
    print("total recorder time: {:.2f}d, {:.0f}h, {:.0f}m, {:.0f}s".format(d,h,m,s))
    select = [
        # 41235,
        # 41236,
        # 41237,
        41238,
        # 41239,
        41240,
        41241,
        41242,
        # 41243,
        41244,
        41245,
        41264,
        41265,
        # 41266,
        41267,
        41268,
        41269,
        41270,
        41271]
    
    # self.df = slt.select_certain_shows(self.df, 'channel_id', select)
    self.df = slt.shows_with_min_time(self.df, 7)
    self.df = slt.drop_unneeded_columns_and_rows(self.df, nan='drop')
    dupes = slt.check_for_duplicates(self.df)
    self.df = slt.drop_shows_from_channel(self.df, 4)
    # self.df = slt.drop_vl(self.df)
    self.df, no = slt.select_shows_w_x_instances(self.df, 10, keep='all')


    channel_target = self.df ['channel_id']
    show_target = self.df ['show_id']
    print(channel_target.shape)
    target = show_target
    select = 'channel_id'
    # no = target.unique().size

    self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id', 'length'], axis=1, inplace=True)

    self.df = self.df.reset_index()
    self._run_scaler()

    ## PCA
    X_kpca = PCA.run_kpca(self.df, 15)
    # X_kpca2d = PCA.run_kpca(self.df, 2)
    # PCA.get_vip_feature_count(self.df, 15, 300)
    # PCA.print_cumsum_trend(self.df, 100, ker='cosine')
    # PCA.print_cumsum_trend(self.df, 100)

    ## TSNE
    perplexity = 110
    X_tsne = tsne.run_tsne(X_kpca, 2, perplexity)
    # X_tsne_300 = tsne.run_tsne(X_kpca, 2, 300)
    # plt.plot_real_clusters(X_tsne_300, channel_target)
    # tsne.tsne_perplexity_test(X_kpca, channel_target , 2)

    data = X_tsne

   
    plt.plot_genre_clusters(data, channel_target)
    # plt.plot_real_clusters(X_kpca, show_target, label='show', title=None)
    # self.run_clusterings_on(self, X, algorithm, args, kwds, select, target)

    # KNN
    # knn._get_nearest_neigbours(X_kpca, y, 4)
    # knn._get_nearest_neigbours(X_tsne2d, y, 4)
    # knn._kkn_cross_validation(X_kpca, y)
    # knn._kkn_cross_validation(X_tsne2d, y)
    # knn.get_neigh(X_tsne, 15, 3)
    # knn._knn_graph(X_tsne, y, 3)
    # knn.draw_roc(X_tsne2d, y, 9)

    # show = 620
    # nearestn = knn.get_neigh(X_kpca, show, 10)
    # print("knn kpca")
    # print(odf.iloc[nearestn, 0:4])


    ## Archetype
    n_arch = 4
    X_train_minmax = np.rot90(data, -1)
    XC, S, C, SSE, varexpl = pcha.PCHA(X_train_minmax, n_arch)
    X_train_minmax = np.rot90(X_train_minmax, 1)
    XC = np.array(XC)
    plt.plot_archetypes(X_train_minmax, channel_target, XC, label='channel', title="Archetypes with tSNE")
    # plt.plot_archetypes(X_train_minmax, channel_target, XC, label='channel', title="Archetypes with tSNE")
    # plt.plot_real_clusters(X_tsne, channel_target, label='channel', title=None)

    a              = arch.Archetypes(self.df)
    archetypesList = a.findAllArchetypes()
    # a.screePlot(title="Scree Test")


if __name__ == "__main__":
    # directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder'
    directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/Database'
    nc = NumberCruncher(directory)
    main(nc)
