import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os
import time

import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MeanShift

import hdbscan


import Archetype as arch
import agglomerative as agg
import PCA
import kmeans
import knn
import tsne


sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

channel_labels = {1: 'BR Klassik',
                2: 'Bayern 1',
                3: 'Bayern 3',
                4: 'B5 Aktuell',
                5: 'Puls',
                6: 'WDR2',
                43: 'WDR3',
                44: 'WDR4'
                }


class NumberCruncher():

    def __init__(self, directory):
        self.directory = directory
        self._load_df('09-11')


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

    def _drop_columns_containing(self, cues):
        # select columns to drop from dataframe
        to_drop = []
        for cue in cues:
            drops = [c for c in self.df.columns if(cue in c)]
            to_drop.extend(drops)
        self.df.drop(to_drop, axis=1, inplace=True)


    def _select_columns_containing(self, cue):
        # select columns to from dataframe which contany keywoard
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
        self._drop_columns_containing(["metadata"])

        self.df = pd.concat([meta_df, self.df], axis=1)
        return self.df


    def select_shows_w_x_instances(self, df, n_min, keep='all'):
        df_selected = pd.DataFrame()
        i=0
        shows = []

        # get all show with more than n_min instances
        for show_id in range(df['show_id'].max()):
            one_show = df[df['show_id'] == show_id]
            if keep != 'all':
                one_show = one_show.head(keep)
            if len(one_show.index) >= n_min:
                i= i+1
                shows.append(show_id)
                df_selected = df_selected.append(one_show)
        print("{} shows with over {} instances: {}".format(i, n_min, shows))
        return df_selected, i

    def select_data_and_target(self):
        y = self.df ['channel_id']
        # drop metadata values
        X = self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id'], axis=1)
        return (X,y)

    def _does_contain_nan(self, df):
        return self.df.isnull().values.any()

    def _check_for_duplicates(self):
        dupes = self.df.duplicated(subset=None, keep= False) #'first')
        print('dupes:', dupes.sum())
        return dupes

    def _drop_duplicates(self):
        self.df.drop_duplicates(keep='first', inplace=True)

    def _select_certain_shows(self, attribute, values):
        df = None
        for i in values:
            shows = self.df[self.df[attribute] == i]
            if df is not None:
                df = df.append(shows, ignore_index=True)
            else:
                df = shows
        return df

    def _drop_shows_from_channel(self, channel_id):
        # drop shows from specified channel
        self.df = self.df[self.df['channel_id'] != channel_id]

    def _drop_vl(self):
        to_drop=["beat count",
              "barkbands",
              "erbbands",
              "gfcc",
              "melbands",
              "mfcc",
              "spectral_contrast_coeffs",
              "spectral_contrast_valleys",
              "beats_loudness_band_ratio",
              "beats_position",
              "hpcp",
              "chords_histogram",
              "thpc"
              ]
        self._drop_columns_containing(to_drop)


    def _drop_unneeded_columns_and_rows(self):
        shape_before = self.df.shape
        to_drop=["beats_position",
                 "mfcc",
                 "dmean2",
                 "dmean",
                 "dvar",
                 "dvar2",
                 "max",
                 "min",
                 "median"
                 ]
        self._drop_columns_containing(to_drop)
        # drop duplicates
        self._drop_duplicates()
        # drop columns without values
        self.df = self.df.dropna(axis=1, how='any')
        rows = shape_before[0] - self.df.shape[0]
        columns = shape_before[1] - self.df.shape[1]
        print("dropped {} rows and {} columns ".format(rows,columns))


    def plot_clusters(self, data, algorithm, args, kwds):
        start_time = time.time()
        labels = algorithm(*args, **kwds).fit_predict(data)
        end_time = time.time()
        palette = sns.color_palette('deep', np.unique(labels).max() + 1)
        colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
        plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        frame = plt.gca()
        plt.axis('off')
        plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=20)
        # plt.text(0.1, 0.9, 'Clustering took {:.2f} s'.format(end_time - start_time), ha='center', va='center', transform=ax.transAxes, fontsize=14)
        plt.show()

    def plot_real_clusters(self, data, target, label=None, title=None):
        palette = sns.color_palette('deep', np.unique(target).max() + 1)
        colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
        plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        plt.axis('off')

        ## add the labels for each group
        if label is not None:
            for i in target.unique():
                # Position of each label.
                xtext, ytext = np.mean(data[target==i], axis=0)
                if label == 'channel':
                    text = channel_labels.get(i)
                    color = 'white'
                    backgroundcolor=palette[i]
                    fontsize=22
                elif label == 'show':
                    text = i
                    color=palette[i]
                    backgroundcolor=(0, 0, 0, 0) # transparent
                    fontsize=18
                plt.annotate(text, (xtext, ytext),
                         horizontalalignment='center',
                         verticalalignment='center',
                         size=fontsize, weight='bold',
                         color=color,
                         backgroundcolor=backgroundcolor)

        if title is not None:
            plt.title('Clusters found by {}'.format(title), fontsize=24)
        plt.show()

    def plot_archetypes(self, data, target, archetypes, label=None, title=None):
        arch_ind = [i[0] for i in archetypes]
        arch_df = data[arch_ind]
        print(arch_df)

        palette = sns.color_palette('deep', np.unique(target).max() + 1)
        colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in target]
        plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
        plt.axis('off')
        plt.scatter(arch_df.T[0], arch_df.T[1], c='r' ,marker='x')
        ## add the labels for each group
        if label is not None:
            for i in target.unique():
                # Position of each label.
                xtext, ytext = np.mean(data[target==i], axis=0)
                if label == 'channel':
                    text = channel_labels.get(i)
                    color = 'white'
                    backgroundcolor=palette[i]
                    fontsize=22
                elif label == 'show':
                    text = i
                    color=palette[i]
                    backgroundcolor=(0, 0, 0, 0) # transparent
                    fontsize=18
                plt.annotate(text, (xtext, ytext),
                         horizontalalignment='center',
                         verticalalignment='center',
                         size=fontsize, weight='bold',
                         color=color,
                         backgroundcolor=backgroundcolor)

        if title is not None:
            plt.title('Clusters found by {}'.format(title), fontsize=24)
        plt.show()


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
    self.df = _load_df2(self.df, directory,'14-11')

    self._clean_df()
    odf = self.df

    # self.df = self._select_certain_shows('channel_id', [4])

    #select shows with certain min length
    length = 60*7 #7 minutes
    self.df = self.df[self.df['length'] >= length]

    self._drop_unneeded_columns_and_rows()
    self._check_for_duplicates()
    self._drop_shows_from_channel(4)
    # self._drop_vl()

    # print(df_klassik)
    self.df, no = self.select_shows_w_x_instances(self.df, 15, keep='all')


    channel_target = self.df ['channel_id']
    show_target = self.df ['show_id']
    target = show_target
    select = 'channel_id'
    # no = target.unique().size

    self.df.drop(['file_name',  'show_id', 'recording_id', 'channel_id', 'length'], axis=1, inplace=True)

    self.df = self.df.reset_index()
    self._run_scaler()

    ## PCA
    X_kpca = PCA.run_kpca(self.df, 15)
    # vif_dict = PCA.select_most_importan_features(self.df, 15, 100)

    ## TSNE
    perplexity = 110
    # X_tsne3d = tsne.run_tsne(X_kpca, 3, perplexity)
    X_tsne = tsne.run_tsne(X_kpca, 2, perplexity)
    # tsne.scatter_tsne_3d(X_tsne3d, y, perplexity)
    # tsne.scatter_tsne(X_tsne, target, perplexity)
    # tsne.tsne_perplexity_test(X_kpca, y , 2)

    # data = X_tsne

    # self.plot_clusters(X_kpca, KMeans, (), {'n_clusters':6})
    # self.plot_clusters(data, DBSCAN, (), {'eps':3.225})
    # self.plot_clusters(data, AffinityPropagation, (), {'preference':-5.0, 'damping':0.95})
    # self.plot_clusters(data, SpectralClustering, (), {'n_clusters': no})
    # self.plot_clusters(data, MeanShift, (0.5,), {'cluster_all':False})
    # self.plot_clusters(X_kpca, hdbscan.HDBSCAN, (), {'min_cluster_size':6})
    #
    #
    # self.plot_real_clusters(X_tsne, show_target, label='show', title=None)
    # self.run_clusterings_on(self, X, algorithm, args, kwds, select, target)


    # KMEANS
    # kmeans.calculate_k_means(X_tsne, no, y)
    # kmeans.calculate_k_means(X_kpca, no, target)
    # kmeans.calculate_k_means_3d(X_tsne3d, no, y)
    # dbscan(X_tsne, y)
    # PCA.print_heatmap(self.df, 20, 400)

    ## AGGLOMERATIVE
    # agg.run_aggloreative_clustering(X_tsne, y, no)
    # agg.run_aggloreative_clustering(X_kpca, no)


    # KNN
    # knn._get_nearest_neigbours(X_kpca, y, 4)
    # knn._get_nearest_neigbours(X_tsne2d, y, 4)
    # knn._kkn_cross_validation(X_kpca, y)
    # knn._kkn_cross_validation(X_tsne2d, y)
    # knn.get_neigh(X_tsne, 15, 3)
    # knn._knn_graph(X_tsne, y, 3)
    # knn.draw_roc(X_tsne2d, y, 9)

    # show = 620
    #
    # nearestn = knn.get_neigh(X_kpca, show, 10)
    # print("knn kpca")
    # print(type(nearestn))
    # print(odf.iloc[nearestn, 0:4])

    # print(X_tsne)

    # # archetypesnp.
    array = self.df.values
    a_abs = np.absolute(array)
    # array = array(self.df.to_records().view(type=np.matrix))
    # print(array)
    a              = arch.Archetypes(array)
    archetypes      = a.findArchetypes(8)
    weights = a.weights()
    print("w", weights)
    arch_ind = [i[0] for i in archetypes]
    print("AA", arch_ind)
    arch_points = X_tsne[arch_ind]
    print(arch_points)
    # print("archetypes", archetypes)
    archetypesList = a.findAllArchetypes()
    # print("archetypes list", archetypesList)
    self.plot_archetypes(X_tsne, channel_target, archetypes)
    # self.plot_archetypes(X_tsne, channel_target, archetypesList)
    # a.weights(k=5, loss='KL');
    a.screePlot()


if __name__ == "__main__":
    # directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder'
    directory = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/Database'
    nc = NumberCruncher(directory)
    main(nc)
