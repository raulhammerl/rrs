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

class put_recordings_in_db():

    def __init__(self, directory):
        directory_db = os.path.join(directory, 'Alternative')
        self.db = Database.Database(directory_db)
        self.directory_captures = os.path.join(directory, 'Data','Captures')
        self.db.init_RadioDB()

    def run(self):
        dirss = []
        for root, dirs, files in os.walk(self.directory_captures):
            dirss.extend(dirs)
            for basename in files:
                if(".mp3" in basename) & ("show" not in basename):
                    channel_name = dirss[0]
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

    def _get_size(self,file):
        tag = TinyTag.get(file)
        return tag.filesize


def main():
    directory = 'TEST/'
    prd = put_recordings_in_db(directory)
    prd.run()

main()
