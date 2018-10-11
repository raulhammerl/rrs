import logging



class MusicFeatureAnalyzer:

    def __init__(directory, ):
        self.directory = directory
        self.df = _load_df()

    def add_show_features_to_df():
        sig = _run_feature_analysis(file)
        csv = _create_df_from_csv(sig)
        _append_to_df(csv)

    def _load_df(file):
        df = pd.read_pickle(df_file)
        return df

    def _save_df():
        df.to_pickle(df_file)

    def _run_feature_analysis(file):
        outputstr = (file.replace(".mp3","") + '.sig')
        outputstr = (outputstr.replace("Caputes","Features"))
        extractor = '/usr/local/bin/essentia_streaming_extractor_music'
        if(os.path.exists(outputstr)==False):
            subprocess.call([ r'/usr/local/bin/essentia_streaming_extractor_music', input, outputstr, '/Users/kingkraul/Dropbox/Documents/Uni/Bachelorarbeit/MusicAnalyzer/extractor_profile.yaml'])
            logging.info('/usr/local/bin/essentia_streaming_extractor_music {} {}'.format(input, outputstr))
        return outputstr


    def _create_df_from_csv(directory):
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

    def _append_to_df(file):
        if(".csv" in file):
            if df is None:
                df = pd.read_csv(file)
            else:
                row = pd.read_csv(file)
                df = df.append(row, ignore_index=True, inplace=True)
        self._save_df(df)

    def run_normalizer(X):
        scaler = Normalizer().fit(X)
        normalizedX = scaler.transform(X)
        return normalizedX

    def _write_to_csv(df, directory):
        file_name = directory + "pandasDF.csv"

        df.to_csv(file_name, encoding='utf-8', index=False)

    def _write_to_excel(pages, directory):
        output = os.path.join(directory, 'output.xlsx')
        writer = pd.ExcelWriter(output)

        i = 0
        for page in pages:
            page.to_excel(writer,('Sheet'+ str(i)))
            i += 1
        writer.save()
