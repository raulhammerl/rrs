import pandas as pd


def drop_columns_containing(df, cues):
    # select columns to drop from dataframe
    to_drop = []
    for cue in cues:
        drops = [c for c in df.columns if(cue in c)]
        to_drop.extend(drops)
    df.drop(to_drop, axis=1, inplace=True)
    return df

def select_columns_containing(df, cue):
    # select columns to from dataframe which contany keywoard
    to_select = [c for c in df.columns if(cue in c)]
    df.loc[:, to_select]
    return df

def select_shows_w_x_instances(df, n_min, keep='all'):
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


def does_contain_nan(df):
    return df.isnull().values.any()

def check_for_duplicates(df):
    dupes = df.duplicated(subset=None, keep= False) #'first')
    print('dupes:', dupes.sum())
    return dupes

def drop_duplicates(df):
    df.drop_duplicates(keep='first', inplace=True)

def select_certain_shows(df, attribute, values):
    df_selected = None
    for i in values:
        shows = df[df[attribute] == i]
        if df_selected is not None:
            df_selected = df_selected.append(shows, ignore_index=True)
        else:
            df_selected = shows
    return df_selected

def drop_shows_from_channel(df, channel_id):
    # drop shows from specified channel
    df = df[df['channel_id'] != channel_id]
    return df

def drop_vl(df):
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
    return drop_columns_containing(df, to_drop)


def drop_unneeded_columns_and_rows(df):
    shape_before = df.shape
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
    drop_columns_containing(df, to_drop)
    # drop duplicates
    drop_duplicates(df)
    # drop columns without values
    df = df.dropna(axis=1, how='any')
    rows = shape_before[0] - df.shape[0]
    columns = shape_before[1] - df.shape[1]
    print("dropped {} rows and {} columns ".format(rows,columns))
    return df

def shows_with_min_time(df, min):
    length = 60*min #make minutes to seconds
    df = df[df['length'] >= length]
    return df
