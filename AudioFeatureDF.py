import pandas as pd


class AudioFeatureDF:

    def __init__(self, directory):
        self.directory = directory
        self.df = self._load_df()

    def _load_df(self):
        df_file = os.path.join(self.directory, 'Data', 'Database', 'music_features.pkl')
        Helpers.create_dir(df_file)

        if os.path.exists(df_file):
            df = pd.read_pickle(df_file)
        else:
            df = None

        return df

    def _save_df(self):
        df_file = os.path.join(self.directory, 'Data', 'Database', 'music_features.pkl')
        self.df.to_pickle(df_file)

    def _clean_df(df):
        #fixing messy column names
        #could also be done by calling columns with: df['name_of_column']
        df.columns = df.columns.str.strip().str.lower().str.replace('.', '_').str.replace('(', '').str.replace(')', '')

        # give boolean value to minor and major chords
        df.tonal_chords_scale = df.tonal_chords_scale.replace({"minor": "0", "major": "1"})
        df.tonal_key_scale = df.tonal_key_scale.replace({"minor": "0", "major": "1"})

        # one hot encode scale key columns
        cols_to_transform = [ 'tonal_chords_key', 'tonal_key_key']
        df = pd.get_dummies(df, columns = cols_to_transform)

        # get metadata columns
        file_name_column = df.metadata_tags_file_name
        show_id_column = df.metadata_tags_album_0
        recording_id_column = df.metadata_tags_tracknumber_0
        channel_id = df.metadata_tags_artist_0
        meta_df = pd.concat([file_name_column, show_id_column, recording_id_column, channel_id], axis=1)
        meta_df.columns = ['file_name',  'show_id', 'recording_id', 'channel_id']

        # drop metadata values
        to_drop = [c for c in df.columns if c.lower()[:8] == 'metadata']
        print(to_drop)
        df = df.drop(to_drop, axis=1)
        df = pd.concat([meta_df, df], axis=1)
        return df
