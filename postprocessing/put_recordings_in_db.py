# from stat import *
import os
import datetime
from tinytag import TinyTag

import Helpers
import Database

"""
* path
* duration
* time created
* channel
"""

channel_names=['BR Klassik','Bayern 1','Bayern 3','B5 Aktuell','Puls','WDR2','WDR3',
'WDR4',"BR_Heimat","Bayern+","Bayern_2_Sued","HR1","HR2","HR3","HR4","You_FM","MDR_Klassik",
"MDR_Jump","MDR_Sputnik","NDR_90.3","NDR2","NDR_Spez","NDR_Blue","NDR1","B888","Fritz", "Radio_Eins"]

class put_recordings_in_db():

    def __init__(self, directory):
        directory_db = os.path.join(directory, 'Alternative')
        self.db = Database.Database(directory_db)
        self.directory_captures = os.path.join(directory, 'Data','Captures')
        self.db.init_RadioDB()

    def run(self):
        for root, dirs, files in os.walk(self.directory_captures):
            for basename in files:
                if(".mp3" in basename) & ("show" not in basename):
                    channel_name = self._get_channel(basename)
                    file = os.path.join( root, basename)
                    t = self._get_creation_time(file)
                    date = t[0]
                    time = t[1]
                    duration = self._get_duration(file)
                    size = self._get_size(file)
                    is_episode = 0
                    channel = self.db.find_channel_by_name(channel_name)
                    print(channel)
                    recording=(
                                channel.id,
                                channel_name,
                                date,
                                time,
                                duration,
                                file,
                                size,
                                is_episode
                    )
                    print(recording)
                    id = self.db.create_recording(recording)
                    print(id)

    def _get_creation_time(self, path):
        t = os.stat(path).st_birthtime
        d = datetime.datetime.fromtimestamp(t)
        d, t = str(d).split(" ")
        return(d,t[:8])

    def _get_duration(self, file):
        tag = TinyTag.get(file)
        duration = int(tag.duration)
        print(duration)
        return Helpers.get_time_from_sec(duration)

    def _get_size(self, file):
        tag = TinyTag.get(file)
        return tag.filesize

    def _get_channel(self, basename):
        for x in channel_names:
            if x in basename:
                channel = x 


        # if('Bayern_1' in basename):
        #     channel = 'Bayern_1'
        # elif('Bayern_3' in basename):
        #     channel = 'Bayern_3'
        # elif('B5_Aktuell' in basename):
        #     channel = 'B5_Aktuell'
        # elif('WDR2' in basename):
        #     channel = 'WDR2'
        # elif('Br_Klassik' in basename):
        #     channel = 'Br_Klassik'
        # elif('Puls' in basename):
        #     channel = 'Puls'
        return channel


def main():
    directory = 'TEST/'
    prd = put_recordings_in_db(directory)
    prd.run()

main()
