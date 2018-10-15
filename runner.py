import sys
import getopt
import os
import logging
import time
import datetime
from subprocess import Popen

import Database
import Entities
import Recorder
import RadioDNS
import AudioDataHandler # edit

logging.basicConfig(level=logging.DEBUG)

def main(argv=None):
        logging.info("\n" * 3 + "="*100)
        logging.info("starting recorder ")

        if argv is None:
            argv = sys.argv

        helpText = '''
        Please enter the following argumets
        [1] name of the channel
        [2] directory to store recordings
        [3] time to record (optional) otherwise recording will continue till 0:00h the next day

        like: "./recorder_exec.py Br_Klassik /User/Data"
        '''

        #too little arguments
        if len(argv) < 3 or len(argv) > 4:
            print(helpText)
            sys.exit()

        channel_name = argv[1]
        directory = argv[2]

        if len(argv) == 4:
            time_to_record = 10 * int(argv[3]) #make minutes

        today = datetime.date.today()
        date = time.strftime('%Y-%m-%d', time.localtime())
        start_time = time.strftime('%H-%M-%S', time.localtime())
        db = Database.Database(directory)
        db.init_RadioDB()
        channel = db.find_channel_by_name(channel_name)

        if channel is None:
            print("There is no channel with that name")
            sys.exit()

        else:
            try:
                # start recording process
                recorder = Recorder.Recorder(today, start_time, channel, directory, time_to_record)
                recording = recorder.capture()

                #start radioDNS parsing
                radioDNS = RadioDNS.RadioDNS(directory, channel, recording, today)
                radioDNS.get_radioDNS_metadata()

                #start audio processing
                # audio_data_handler = Audio_data_handler.Audio_data_handler(directory, today, channel)
                # audio_data_handler.cut_blob_into_episodes()

            except RuntimeError as e:
              exit("ERROR: {}".format(e.message))

            digester = "/Users/Raul/rrs/digesting_runner.py"
            Popen(['python3', digester, directory, date, channel_name])

if __name__ == "__main__":
    main()
