import MusicFeatureAnalyzer
import Audio_data_handler


def main():

    audio_data_handler = Audio_data_handler.Audio_data_handler(db, db_conn, date, channel)
    audio_data_handler.cut_blob_into_episodes(db, db_conn, today, channel)

    music_feature_analyzer = MusicFeatureAnalyzer
    music_feature_analyzer.add_show_features_to_df():
