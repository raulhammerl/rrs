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

import sys
import logging
import os

import AudioDataHandler
import MusicFeatureAnalyzer
import Database
import RadioDNS
from datetime import date, timedelta

logging.basicConfig(level=logging.INFO)


def main(argv=None):
    if argv is None:
        argv = sys.argv


    helpText ='''
    Please enter the following argumets
    [1] channel name
    [2] directory
    [3] date
    like: "./digsting_runner.py /User/Data 2018-02-10 Br_Klassik"
    '''

    #too little arguments
    if len(argv) != 3: #4
        print(helpText)
        sys.exit()

    channel_name = argv[1]
    directory = argv[2]
    # date = argv[2]
    yesterday = str(date.today() - timedelta(1))
    print(yesterday)
    print(type(yesterday))

    digest_daily_blob(directory, yesterday, channel_name)


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



    logging.info("Digesting process finished")
    sys.exit(0)



if __name__ == "__main__":
    main()
