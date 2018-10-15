import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError
import urllib.request
import os
import os.path

import logging


from Entities import Episode, Channel
import Database
import Helpers


class RadioDNS:

    def __init__(self, directory, channel, recording, date):
        self.db = Database.Database(directory)
        self.recording = recording
        self.channel = channel
        self.date = str(date)
        self.directory = directory
        self.directory = os.path.join(directory, 'Captures')


    def get_radioDNS_metadata(self):
        radioDNS_url = self._get_url()
        logging.debug("got rDNS url {} for {}".format(radioDNS_url, self.channel.name))
        radionDNS_xml = self._catch_radioDNS(radioDNS_url)
        logging.debug("got rDNS XMl for {}".format(self.channel.name))
        #change recording.filename to RDNS_path so recording can be created afterwards
        self._read_radioDNS(radionDNS_xml)
        logging.debug("interpreted rDNS XMl for {}".format(self.channel.name))

    def _catch_radioDNS(self, radioDNS_url):
        """
        Safe radioDNS XML to file
        :param channel:
        :param radioDNS_url:
        :param target_path:
        :return:
        """
        slug = os.path.join(
            self.channel.name,
            self.date,
            "{}_{}.xml".format(
                self.channel.name,
                self.date
            )
        )

        filename = os.path.join(self.directory, slug)


        try:
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)

            urllib.request.urlretrieve(radioDNS_url, filename)

        except Exception as e:
            logging.error("Could not capture show metadata (radioDNS) from {}, \n because an exception occured: {}".format(radioDNS_url, e))
            raise e

        return filename

    def _get_url(self):
        base_url = self.channel.radiodns_url
        date = self.date.replace("-","")
        radioDNS_url = base_url + "{}_PI.xml".format(date)
        return radioDNS_url


    def _read_radioDNS(self, radioDNS_xml):
        #ueberpruefen ob datum in XML == Datum URL
        with open(radioDNS_xml, 'rb') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()

        namespaces = {'wdab': 'http://www.worlddab.org/schemas/spi/31', }
        programmes = root.findall('.//wdab:schedule/wdab:programme', namespaces)



        #read programm information and safe to database
        for program in programmes:
            #if else longName
            #was passiert bei NONE?

            time_attr = program.find('.//wdab:location/wdab:time', namespaces)
            episode_time = time_attr.get('time')
            date = episode_time[:10]
            episode_time = episode_time[11:19]
            duration = time_attr.get('duration')
            duration = duration[2:]

            ## time formating for comparison
            recording_start_time = Helpers.get_sec(self.recording.start_time)
            recording_end_time = recording_start_time + Helpers.get_sec(self.recording.duration)
            episode_start_time = Helpers.get_sec(episode_time)
            episode_end_time = episode_start_time + Helpers.get_sec_from_duration(duration)

            # check if episode ended before recording started
            if(episode_end_time < recording_start_time): continue
            # check if episode episode starts after recording ended
            if(episode_start_time > recording_end_time): break


            mediumName_attr = program.find('wdab:mediumName', namespaces)
            name = mediumName_attr.text

            genres = program.findall('wdab:genre', namespaces)
            genre_string = ""

            # append all given genres to one string
            for i in genres:
                genre_string += i.text.rstrip()

            media_description_attr = program.find('.//wdab:mediaDescription', namespaces) #change name

            if media_description_attr is not None:
                if media_description_attr.find('.//wdab:longDescription', namespaces) is not None:
                    media_description_attr = media_description_attr.find('wdab:longDescription', namespaces)

                else:
                    media_description_attr = media_description_attr.find('wdab:shortDescription', namespaces)

                media_description = media_description_attr.text

            else:
                media_description = 'keine'

            # find show_id. If show does not exist yet, create a new show
            show_id_tupel = self.db.find_show(name)
            print("show tuple {}".format(show_id_tupel))
            logging.info("looking for show with name: {}".format(name))

            if show_id_tupel is None:
                newShow = (self.channel.id, name, genre_string, 'de', 'unknown') #EDIT 'unknown'
                show_id = self.db.create_show(newShow)
            else:
                show_id = show_id_tupel[0]

            newEpisode = (show_id, media_description, self.date , duration, self.recording.id, episode_time)
            newEpisode_id = self.db.create_episode(newEpisode)
