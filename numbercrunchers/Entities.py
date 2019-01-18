import datetime
import time
import os

class Episode(object):
    """
    Describes an episode of a show.
    """
    def __init__(self, show_id, description, date, duration, recording_id, start_time):
        # if not isinstance(show, Show):
        # raise TypeError('show has to be of type "Show"')
        self.id = id
        self.duration = duration
        self.start_time = start_time
        self.description = description
        self.show_id = show_id
        self.date = date
        self.recording_id = recording_id

class Show(object):
    """
    Describes a show of a channel.
    """
    def __init__(self, stream_url, name, description):
        self.stream_url = stream_url
        self.id = id
        self.name = name
        self.keywords = []
        self.episodes = []
        self.description = description

class Channel(object):
    """
    Describes an instance of a radio channel.
    """
    def __init__(self, name, description, language, stream_url, radiodns_url):
        #super(Channel, self).__init__()??
        self.stream_url = stream_url
        self.radiodns_url = radiodns_url
        self.id = id
        self.description = description
        self.name = name
        self.shows = []
        self.language = language

    def __repr__ (self):
        return ('Channel:: ID:{} Name:{} Description{} Language:{} Stream:{} RadioDNS:{}'
        .format(self.id, self.name, self.description, self.language, self.stream_url, self.radiodns_url))

class Recording(object):
    """
    Describes an instance of a channels recording.
    """
    def __init__(self, channel_id, date, start_time, duration, file, is_episode):
        date_pattern = "%Y-%m-%d"
        self.channel_id = channel_id
        self.date = date
        self.start_time = start_time
        self.duration = duration
        # self.file_name = "{}, {}".format(channel.name, time.strftime(date_pattern, date))
        # self.slug = os.path.join(
        #     channel_name,
        #     str(date),
        #     # str(start_time),
        #     "{}_{}.mp3".format(
        #         self.channel_name, #slugify(self.channel.name),
        #         str(start_time)
        #     )
        # )
        self.file = file
        self.is_episode = is_episode
        self.id = None
        self.file_size = 0

    def __repr__ (self):
        if self.id is not None:
            return ('Recording:: ID:{} channel:{} date:{} start time:{} duration:{} file:{} is_episode:{}'
            .format(self.id, self.channel_id, self.date, self.start_time, self.duration, self.file, self.is_episode))
        else:
            return ('Recording:: channel:{} date:{} start time:{} duration:{} file:{} is_episode:{}'
            .format(self.channel_id, self.date, self.start_time, self.duration, self.file, self.is_episode))
