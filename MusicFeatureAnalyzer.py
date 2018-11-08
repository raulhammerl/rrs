import logging
import os
import subprocess
import pandas as pd
from pathlib import Path
home = str(Path.home())
if ('root' in home):
    home = '/Users/kingkraul'


import AudioFeatureDF
import Helpers


class MusicFeatureAnalyzer:

    def __init__(self, directory):
        self.directory = directory
        # self.df = AudioFeatureDF.AudioFeatureDF(directory)
        self.df = self._load_df()


    def analyze_episode(self, file):
        sig = self._run_feature_analysis(file)
        csv = self._create_csv_from_sig(sig)
        self._append_to_df(csv)
        self._save_df()

    def _load_df(self):
        df_file = os.path.join(self.directory, 'Data', 'Database', 'music_features.pkl')
        Helpers.create_dir(df_file)

        if os.path.exists(df_file):
            with open(df_file, 'rb') as f:
                df = pd.read_pickle(f)
        else:
            df = None

        return df

    def _save_df(self):
        df_file = os.path.join(self.directory, 'Data', 'Database', 'music_features.pkl')
        with open(df_file, 'wb') as f:
            self.df.to_pickle(f)

    def _run_feature_analysis(self, input):
        outputstr = (input.replace(".mp3","") + '.sig')
        outputstr = (outputstr.replace("Extracts", "Features"))
        Helpers.create_dir(outputstr)

        extractor = '/usr/local/bin/essentia_streaming_extractor_music'
        try:
            if(os.path.exists(outputstr)==False):
                subprocess.call([ r'/usr/local/bin/essentia_streaming_extractor_music', input, outputstr, home+ '/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/extractor_profile.yaml'])
                logging.debug(' features being analyzed from: {} to: {}'.format(input, outputstr))
            return outputstr

        except OSError as e:
          exit("ERROR: {}".format(e.message))



    def _create_csv_from_sig(self, input):
        """metadata.audio_properties.* metadata.tags.musicbrainz_recordingid.0"""
        include = "--include lowlevel.* rhythm.* tonal.* "
        ignore = "--ignore *.min *.min.* *.max *.max.* *.dvar *.dvar2 *.dvar.* *.dvar2.* *.dmean *.dmean2 *.dmean.* *.dmean2.* *.cov.* *.icov.* rhythm.beats_position.* "
        try:
            if(".sig" in input):
                output = input.replace(".sig",".csv")
                if(os.path.exists(output)==False):
                    call = ["/usr/local/bin/python3", home+'/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/json_to_csv.py', '-i',input ,'-o', output, "--ignore", "rhythm.beats_position.*", "*mfcc*"]
                    subprocess.call(call)
                    logging.debug(call)

            return output

        except OSError as e:
            exit("ERROR: {}".format(e.message))



    def _create_df_from_csv(self, directory):
        df = None
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if(".csv" in basename):
                    try:
                        file = os.path.join(root, basename)
                        print(file)
                        if df is None:
                            df = pd.read_csv(file)
                        else:
                            row = pd.read_csv(file)
                            df = df.append(row, ignore_index=True)
                    except pd.errors.EmptyDataError as e:
                        logging.warning("could not read csv {} because {}".format(file, e))
        return df


    def _append_to_df(self, file):
        if(".csv" in file):
            if self.df is None:
                self.df = pd.read_csv(file)
                # self.df = self._clean_df(df)
                logging.debug("no df found, so a new one was created from: {}".format(file))
            else:
                row = pd.read_csv(file)
                # row = self._clean_df(row)
                self.df = self.df.append(row, ignore_index=True)
                logging.debug("row appended to df: {}".format(file))
        self._save_df()

    def _run_normalizer(self, X):
        scaler = Normalizer().fit(X)
        normalizedX = scaler.transform(X)
        return normalizedX

    def _write_to_csv(self, df, directory):
        file_name = directory + "pandasDF.csv"
        df.to_csv(file_name, encoding='utf-8', index=False)

    def _write_to_excel(self, pages, directory):
        output = os.path.join(directory, 'output.xlsx')
        writer = pd.ExcelWriter(output)

        i = 0
        for page in pages:
            page.to_excel(writer,('Sheet'+ str(i)))
            i += 1
        writer.save()

    def _clean_df(self, df):
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

# def main():
#     directory = '/Users/Raul/Features'
#     MFA = MusicFeatureAnalyzer(directory)
#     df = MFA._create_df_from_csv(directory)
#     MFA._append_to_df()
#
#
# if __name__ == "__main__":
#     main()
