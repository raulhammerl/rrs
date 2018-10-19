




class NumberCruncher():

    def __init__(self, directory):
        self.directory = directory

        self._load_df('df')


    def _load_df(self, name):
        df_file = os.path.join(self.directory,'Data','Database', name, '.pkl')
        self.df = pd.read_pickle(df_file)


    def _run_normalizer(self):
        scaler = Normalizer().fit(X)
        normalizedX = scaler.transform(X)
        return normalizedX


    def _drop_mfccs(self):
        to_drop = [c for c in self.df.columns if("mfcc" in c)]
        # print(to_drop)
        self.df.drop(to_drop, axis=1, inplace=True)

    def _drop_beat_positions(self):
        to_drop = [c for c in self.df.columns if("beats_position" in c)]
        # print(to_drop)
        self.df.drop(to_drop, axis=1, inplace=True)


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
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


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
