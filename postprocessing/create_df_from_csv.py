import pandas as pd
import os

def create_df_from_csv(directory):
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
                except pd.errors.EmptyDataError:
                    print("file empty")
                    continue

    return df

def main():
    directory = 'Volumes/Untitled/BA/Data/Features'
    df_file = 'Volumes/Untitled/BA/Data/Database/manual.pkl'
    df = create_df_from_csv(directory)
    df.to_pickle(df_file)

main()
