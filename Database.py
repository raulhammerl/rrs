import sqlite3
from sqlite3 import Error
import os.path
import os
import logging

from Entities import Episode, Channel, Recording

class dbopen(object):
    """
    CM for database. Commits everything at exit.
    """
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


class Database:

    def __init__(self, db_file):
        self.db_file = db_file

    def execute(self, statement, values, fetch):
        with  dbopen(self.db_file) as c:
            try:
                if values is None:
                    c.execute(statement)
                else:
                    c.execute(statement, values)

                if fetch == 'lastrow':
                    data = c.fetchall()
                if fetch == 'allrows':
                    data = c.fetchall()
                if fetch == 'onerow':
                    data = c.fetchone()
                if fetch is None:
                    data = None
                return data
            except sqlite3.Error as e:
                logging.warning(e)



    def create_table(self, create_table_sql):
        """create a table from the create_table_sql statement"""
        self.execute(create_table_sql, None, None)

    def create_recording (self, recording):
        """
        Create a new recording
        :param recording:
        :return:
        """
        sql = ''' INSERT INTO recordings(channel_id, channel_name, recording_date, start_time, duration, file_path, file_size, is_episode)
                  VALUES(?,?,?,?,?,?,?,?) '''
        data = self.execute(sql, recording, 'lastrow')
        return data

    def find_recording(self, id):
        sql = '''SELECT * FROM recordings WHERE recording_id = ? '''
        recording_tuple = self.execute(sql, [id], 'onerow')

        if recording_tuple is None:
            logging.info("Could not find recording: {}".format(id))
            return None
        else:
            #create epsiode entity
            recording = Recording(recording_tuple[1], recording_tuple[3], recording_tuple[4], recording_tuple[5], recording_tuple[6], recording_tuple[8])
            recording.id = id
            recording.channel_name = recording_tuple[2]
            logging.info("{} found".format(recording))
            return recording


    def find_recordings_by_date(self, date):
        sql = 'SELECT * FROM recordings WHERE recording_date = ? '
        data = self.execute(sql, [date], 'allrows')
        return data

    def update_recording_path(self, id, path):
        sql = '''UPDATE recordings
                 SET file_path = ?
                 WHERE recording_id = ?'''
        with dbopen(self.db_file) as c:
            data = c.execute(sql,[path, id], 'lastrow')
            return data


    def create_channel(self, channel):
        """
        Create a new channel
        :param conn:
        :param channel:
        :return:
        """
        sql = ''' INSERT INTO channels(name, description, language, stream_url, radiodns_url)
                  VALUES(?,?,?,?,?) '''
        data = self.execute(sql, channel, 'lastrow')
        return data

    def delete_channel(self, channel_id):
        """
        Delete a channel by channel id
        :param conn:  Connection to the SQLite database
        :param id: id of the channel
        :return:
        """
        sql = '''DELETE FROM channels WHERE channel_id=?'''
        self.execute(sql, [channel_id], None)


    def find_channel_by_name (self, channel_name):
        sql = '''SELECT * FROM channels WHERE name=?'''
        self.execute(sql, [channel_name], None)
        #EDIT probleme wenn doppelt gefunden
        channel_tuple = self.execute(sql, [channel_name], 'onerow')
        if channel_tuple is None:
            logging.info("Could not find channel: {}".format(channel_name))
            return None
        else:
            #create channel entity
            channel = Channel(channel_tuple[1], channel_tuple[2], channel_tuple[3], channel_tuple[4],channel_tuple[5])
            channel.id = channel_tuple[0]
            logging.info("{} found".format(channel))
            return channel

    def find_channel (self, channel_id):
        sql = '''SELECT * FROM channels WHERE channel_id=?'''
        #EDIT probleme wenn doppelt gefunden
        channel_tuple = self.execute(sql, [channel_id], 'onerow')
        if channel_tuple is None:
            logging.info("Could not find channel: {}".format(channel_id))
            return None
        else:
            #create channel entity
            channel = Channel(channel_tuple[1], channel_tuple[2], channel_tuple[3], channel_tuple[4],channel_tuple[5])
            channel.id = channel_tuple[0]
            logging.info("{} found".format(channel))
            return channel

    def list_channels (self):
        sql = '''SELECT channel_id, name FROM channels WHERE channel_id=?'''
        channels = self.cur.execute(sql, (channel_id,), 'allrows')
        print(channels)

    def create_show(self, show):
        """
        Create a new show
        :param conn:
        :param show:
        :return:
        """
        sql = ''' INSERT INTO shows(channel_id, name, genre, language, keywords)
                  VALUES(?,?,?,?,?) '''
        data = self.execute(sql, show, 'lastrow')
        return data

    def find_show (self, show_name):
        sql = 'SELECT rowid FROM shows WHERE name=?'
        data = self.execute(sql, [show_name],'onerow')
        #EDIT probleme wenn doppelt gefunden
        return data

    def delete_show(self, show_id):
        """
        Delete a show by show id
        :param conn:  Connection to the SQLite database
        :param id: id of the show
        :return:
        """
        sql = 'DELETE FROM shows WHERE show_id=?'
        self.execute(sql, [show_id], None)



    def create_episode(self, episode):
        """
        Create a new episode
        :param conn:
        :param episode:
        :return:
        """
        sql = ''' INSERT INTO episodes(show_id, description, date, duration, recording_id, start_time)
                  VALUES(?,?,?,?,?,?) '''
        data = self.execute(sql, episode, 'lastrow')
        return data


    def find_episode_by_id(self, id):
        sql = '''SELECT * FROM episodes WHERE episode_id = ? '''
        episode_tuple = self.execute(sql, [id], 'onerow')
        if episode_tuple is None:
            logging.info("Could not find episode: {}".format(id))
            return None
        else:
            #create epsiode entity
            episode = Episode(episode_tuple[1], episode_tuple[2], episode_tuple[3], episode_tuple[4], episode_tuple[5], episode_tuple[6])
            episode.id = id
            logging.info("{} found".format(episode))
            return episode


    def find_episodes_by_date(self, date):
        sql = 'SELECT * FROM episodes WHERE date = ? '
        data = self.execute(sql, [date], 'allrows')
        return data

    def update_episode_recording(self, episode_id, recording_id):
        sql = '''UPDATE episodes
                 SET  recording_id = ?
                 WHERE episode_id = ?'''
        print("updating episode: {} to recording: {}".format(episode_id, recording_id))
        data = self.execute(sql,[recording_id, episode_id], 'lastrow')
        return data

    def delete_episode(self, episode_id):
        """
        Delete a episode by episode id
        :param conn:  Connection to the SQLite database
        :param id: id of the episode
        :return:
        """
        sql = 'DELETE FROM episodes WHERE episode_id=?'
        self.execute(sql, [episode_id], None)

    def delete_recording(self, recording_id):
        """
        Delete a episode by episode id
        :param conn:  Connection to the SQLite database
        :param id: id of the episode
        :return:
        """
        sql = 'DELETE FROM episodes WHERE recording_id=?'
        self.execute(sql, [recording_id], None)

    def init_RadioDB(self, db_file):
        sql_channels = '''CREATE TABLE if not exists channels(
        channel_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        language TEXT,
        stream_url TEXT,
        radiodns_url TEXT
        );'''

        sql_shows = '''CREATE TABLE if not exists shows(
        show_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        name TEXT,
        genre TEXT,
        language TEXT,
        keywords TEXT,
        FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
        );'''

        sql_episodes = '''CREATE TABLE if not exists episodes(
        episode_id INTEGER PRIMARY KEY,
        show_id INTEGER,
        description TEXT,
        date TEXT,
        duration Text,
        recording_id TEXT,
        start_time TEXT,
        FOREIGN KEY (show_id) REFERENCES shows(show_id)
        );'''

        sql_recordings = '''CREATE TABLE if not exists recordings(
        recording_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        channel_name TEXT,
        recording_date TEXT,
        start_time TEXT,
        duration TEXT,
        file_path TEXT,
        file_size NUMERIC,
        is_episode INTEGER,
        FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
        );'''


        self.create_table(sql_channels)
        self.create_table(sql_shows)
        self.create_table(sql_episodes)
        self.create_table(sql_recordings)

        #initial channels
        channel = ("Br_Klassik", "Klassik", "de",
         "http://br-brklassik-live.cast.addradio.de/br/brklassik/live/mp3/128/stream.mp3",
         "http://epg4br.irt.de/radiodns/spi/3.1/dab/de0/10a5/d314/0/")
        channel_id = self.create_channel(channel)


        channel = ("Bayern_1", "", "de",
            "http://br-br1-mainfranken.cast.addradio.de/br/br1/mainfranken/mp3/128/stream.mp3",
            "http://epg4br.irt.de/radiodns/spi/3.1/dab/de0/1131/d711/0/")
        channel_id = self.create_channel(channel)


        channel = ("Bayern_3", "", "de",
            "http://br-br3-live.cast.addradio.de/br/br3/live/mp3/128/stream.mp3",
            "http://epg4br.irt.de/radiodns/spi/3.1/dab/de0/10a5/d313/0/")
        channel_id = self.create_channel(channel)


        channel = ("B5_Aktuell", "", "de",
            "http://br-b5aktuell-live.cast.addradio.de/br/b5aktuell/live/mp3/128/stream.mp3",
            "http://epg4br.irt.de/radiodns/spi/3.1/dab/de0/10a5/d315/0/")
        channel_id = self.create_channel(channel)


        channel = ("Puls", "", "de",
            "http://br-puls-live.cast.addradio.de/br/puls/live/mp3/128/stream.mp3",
            "http://epg4br.irt.de/radiodns/spi/3.1/dab/de0/10a5/d317/0/")
        channel_id = self.create_channel(channel)

        channel = ("WDR2", "", "de",
            "http://wdr-wdr2-rheinland.icecast.wdr.de/wdr/wdr2/rheinland/mp3/128/stream.mp3",
            "http://epg4wdr.irt.de/radiodns/spi/3.1/dab/de0/1019/d392/0/"
            )
        channel_id = self.create_channel(channel)

    def init_episodes(self):
        sql_episodes = '''CREATE TABLE if not exists episodes(
        episode_id INTEGER PRIMARY KEY,
        show_id INTEGER,
        description TEXT,
        date TEXT,
        duration Text,
        recording_id TEXT,
        start_time TEXT,
        FOREIGN KEY (show_id) REFERENCES shows(show_id)
        );'''

        self.create_table(sql_episodes)

    def printDB(self):
        select_channels_sql = "SELECT * FROM channels;"
        select_shows_sql = "SELECT * FROM shows;"
        select_episodes_sql = "SELECT * FROM episodes;"
        data = self.execute(select_channels_sql , None, 'allrows')
        print(data)
        data = self.execute(select_shows_sql , None, 'allrows')
        print(data)
        data = self.execute(select_episodes_sql , None, 'allrows')
        print(data)

# def main():
#     cwd = os.getcwd()
#     print("cwd {}".format(cwd))
#     db = Database()
#     db_file = os.path.join(cwd, 'self.sqlite')
#     conn = self.create_connection(db_file)
#
#     self.init_RadioDB(db_file)
#     self.printDB(db_file)
#     # channel = self.find_channel(conn, "BR_KLASSIK")
#     # print(channel)
# main()
