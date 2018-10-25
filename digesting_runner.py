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

logging.basicConfig(level=logging.DEBUG)


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

    if len(argv) < 3 or len(argv) > 4:
        print(helpText)
        print(len(argv))
        sys.exit()

    channel_name = argv[1]
    directory = argv[2]

    print(argv)
    print(len(argv))

    if len(argv) == 4:
        yesterday = argv[3]
    else:
        yesterday = str(date.today() - timedelta(1))
        print(yesterday)
        print(type(yesterday))

    digest_daily_blob(directory, yesterday, channel_name)


def digest_daily_blob(directory, date, channel_name):
    db = Database.Database(directory)
    # find all recordigns from date
    all_recordings = db.find_recording_by_date_and_channel(date, channel_name)
    print(all_recordings)
    for recording in all_recordings:
        # get recording entity
        recording_id = recording[0]
        recording = db.find_recording(recording_id)
        logging.debug("Recording found: {}".format(recording))
        # if(recording.channel == channel_name):
        # start radioDNS parsing
        radioDNS = RadioDNS.RadioDNS(directory, channel_name, recording, date)
        radioDNS.get_radioDNS_metadata()

    # find all episodes from date
    all_rows = db.find_episodes_by_date(date)
    logging.debug("trying to find episodes with date: {}".format(date))

    for episode in all_rows:
        #get episode entity
        episode_id = episode[0]
        episode = db.find_episode_by_id(episode_id)
        logging.debug("found episode with id: {}".format(episode_id))

        # find corresponding recording
        recording = db.find_recording(episode.recording_id)
        logging.debug("Recording found: {}".format(recording))

        ##try
        # check if recording is already an extract if so skip episode
        try:
            if recording.is_episode is 1: #is episode to is_analized
                logging.debug("recording is already an episode")
                continue

            audio_data_handler = AudioDataHandler.AudioDataHandler(directory, date, channel_name)
            extracted_episode = audio_data_handler.extract_episode(episode, recording)

            if extracted_episode is not None:
                music_feature_analyzer = MusicFeatureAnalyzer.MusicFeatureAnalyzer(directory)
                music_feature_analyzer.analyze_episode(extracted_episode)
            else:
                logging.warning("episoded could not be extracted")


        except RuntimeError as e:
          exit("ERROR: {}".format(e.message))


    logging.info("Digesting process finished")
    sys.exit(0)



if __name__ == "__main__":
    main()
