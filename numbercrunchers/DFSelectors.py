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
