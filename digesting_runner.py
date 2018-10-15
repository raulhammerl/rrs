import sys
import logging

import AudioDataHandler
import MusicFeatureAnalyzer
import Database

"""

needs:
* DB
* date
* channel


all_rows = self.db.find_episodes_by_date(self.date)

    data_handler:
        * date
        * episode
        * recording

    feature_analyzer
        * directory
        * episode_path

"""


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #too little arguments
    if len(argv) != 4:
        print(helpText)
        sys.exit()
    directory = argv[1]
    date = argv[2]
    channel_name = argv[3]
    digest_daily_blob(directory, date, channel_name)


def digest_daily_blob(directory, date, channel_name):
    db = Database.Database(directory)
    # find all episodes from date
    all_rows = db.find_episodes_by_date(date)
    logging.debug("trying to find episodes with date: {}".format(date))

    for episode in all_rows:
        #get episode attributes
        episode_id = episode[0]
        episode = db.find_episode_by_id(episode_id)
        logging.debug("found episode with id: {}".format(episode_id))

        # find corresponding recording
        recording = db.find_recording(episode.recording_id)
        logging.debug("Recording found: {}".format(recording))


        # check if recording is already an extract if so skip episode
        if recording.is_episode is 1: #is episode to is_analized
            logging.debug("recording is already an episode")
            continue

        audio_data_handler = AudioDataHandler.AudioDataHandler(directory, date, channel_name)
        extracted_episode = audio_data_handler.extract_episode(episode, recording)

        if extracted_episode is not None:
            music_feature_analyzer = MusicFeatureAnalyzer.MusicFeatureAnalyzer(directory)
            music_feature_analyzer.analyze_episode(extracted_episode)




if __name__ == "__main__":
    main()
