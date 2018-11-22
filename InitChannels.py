import csv
import requests

# import Database

def init_RadioDB(self):
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

    channel = ("WDR3", "Klassik", "de",
        "http://wdr-wdr3-live.icecast.wdr.de/wdr/wdr3/live/mp3/128/stream.mp3?ar-distributor=ffa1",
        "http://epg4wdr.irt.de/radiodns/spi/3.1/dab/de0/10ec/d393/0"
        )
    channel_id = self.create_channel(channel)

    channel = ("WDR4", "Schlager", "de",
        "http://wdr-wdr4-live.icecast.wdr.de/wdr/wdr4/live/mp3/128/stream.mp3?ar-distributor=ffa1",
        "http://epg4wdr.irt.de/radiodns/spi/3.1/dab/de0/1019/d392/0/"
        )
    channel_id = self.create_channel(channel)

    channel = ("Antenne", "Schlager", "de",
        "http://mp3channels.webradio.antenne.de:80/antenne",
        "https://www.antenne.de/radiodns/spi/3.1/dab/de0/10a5/d318/0/"
        )
    channel_id = self.create_channel(channel)

def read_channel_csv():
    array = []
    selfcsv_file = "/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/RadioDNS/DabandStreams.csv"
    with open(selfcsv_file, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                name = row[0].replace(" ","")
                dab = row[1].replace(".","/").replace(":","/")
                stream_url = row[2].replace(" ","")
                channel_url = row[3].replace(" ","")
                radiodns_url = channel_url + dab
                array.append(name)
                channel = (
                    name,
                    "",
                    "de",
                    stream_url,
                    radiodns_url
                )
                radiodns_url = radiodns_url + "20181122_PI.xml"
                request = requests.get(stream_url, stream=True)
                if request.status_code == 200:
                    print(name,': Web site exists', stream_url)
                    # pass
                else:
                    print(name,': Web site does not exist', stream_url)
                # Database.create_channel(channel)
                line_count += 1
        print(f'Processed {line_count} lines.')
        print(array)


read_channel_csv()
