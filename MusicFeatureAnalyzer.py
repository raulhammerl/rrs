import logging
import os
import subprocess
import pandas as pd

import Helpers


class MusicFeatureAnalyzer:

    def __init__(self, directory):
        self.directory = directory
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
            df = pd.read_pickle(df_file)
        else:
            df = None

        return df

    def _save_df(self):
        df_file = os.path.join(self.directory, 'Data', 'Database', 'music_features.pkl')
        self.df.to_pickle(df_file)

    def _run_feature_analysis(self, input):
        outputstr = (input.replace(".mp3","") + '.sig')
        outputstr = (outputstr.replace("Captures","Features"))
        Helpers.create_dir(outputstr)

        extractor = '/usr/local/bin/essentia_streaming_extractor_music'
        if(os.path.exists(outputstr)==False):
            subprocess.call([ r'/usr/local/bin/essentia_streaming_extractor_music', input, outputstr, '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/extractor_profile.yaml'])
            logging.debug('/usr/local/bin/essentia_streaming_extractor_music {} {}'.format(input, outputstr))
        return outputstr

    def _create_csv_from_sig(self, input):
        include = "--include metadata.audio_properties.* metadata.tags.musicbrainz_recordingid.0 lowlevel.* rhythm.* tonal.* "
        ignore = "--ignore *.min *.min.* *.max *.max.* *.dvar *.dvar2 *.dvar.* *.dvar2.* *.dmean *.dmean2 *.dmean.* *.dmean2.* *.cov.* *.icov.* rhythm.beats_position.* "
        # outputstr = '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/{}.csv'.format(output)
        if(".sig" in input):
            output = input.replace(".sig",".csv")
            if(os.path.exists(output)==False):
                call = ["/usr/local/bin/python3", '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/json_to_csv.py', '-i',input ,'-o', output]
                subprocess.call(call)
                logging.debug(call)

        return output




    def _create_df_from_csv(self, directory):
        df = None
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if(".csv" in basename):
                    file = os.path.join(root, basename)
                    if df is None:
                        df = pd.read_csv(file)
                    else:
                        row = pd.read_csv(file)
                        df = df.append(row, ignore_index=True)

        return df


    def _append_to_df(self, file):
        if(".csv" in file):
            if self.df is None:
                self.df = pd.read_csv(file)
            else:
                row = pd.read_csv(file)
                self.df = self.df.append(row, ignore_index=True)
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
