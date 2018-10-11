import sys
import getopt
import os
import logging
import time
import datetime

import Database
import Entities
import Recorder
import RadioDNS
import Audio_data_handler

logging.basicConfig(level=logging.DEBUG)



def main(argv=None):
        logging.info("\n" * 3 + "_"*100)
        logging.info("starting recorder ")

        if argv is None:
            argv = sys.argv

        helpText = '''
        Please enter the
        [1] name of the channel
        [2] minutes to record
        [3] directory to store recordings
        as arguments


        like: "./recorder_exec.py Br_Klassik 1440 /User/Data"
        '''

        #too little arguments
        if len(argv) != 4:
            print(helpText)
            sys.exit()

        channel_name = argv[1]
        time_to_record = 60 * int(argv[2])
        directory = argv[3]


        today = datetime.date.today()
        date = time.strftime('%Y-%m-%d', time.localtime())
        start_time = time.strftime('%H-%M-%S', time.localtime())
        db_file = os.path.join(directory, 'Database', 'db.sqlite')

        db = Database.Database(db_file)
        db.init_RadioDB(db_file)
        channel = db.find_channel_by_name(channel_name)

        if channel is None:
            print("There is no channel with that name")
            sys.exit()

        else:
            try:
                # maybe put retryer here?!
                # start recording process
                recorder = Recorder.Recorder(db_file, today, start_time, channel, time_to_record, directory)
                recording = recorder.capture()

                #start radioDNS parsing
                radioDNS = RadioDNS.RadioDNS(db_file, channel, directory, recording, today)
                radioDNS.get_radioDNS_metadata()

                #start audio processing
                audio_data_handler = Audio_data_handler.Audio_data_handler(db_file, today, channel)
                audio_data_handler.cut_blob_into_episodes(db_file, today, channel)

            except RuntimeError as e:
              exit("ERROR: {}".format(e.message))

if __name__ == "__main__":
    main()
