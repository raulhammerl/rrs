import datetime
import logging
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from socket import timeout

from Entities import Episode, Recording, Channel
import Database
import Helpers
import NetworkError


@NetworkError.retryer(max_retries=7, timeout=12)
class Recorder:

        def __init__(self, db_file, today, start_time, channel , duration, directory):
            #get database connection
            self.db = Database.Database(db_file)
            self.channel = channel
            self.today = today
            self.duration = duration
            self.start_time = start_time
            self.directory = directory
            self.duration = duration

            self.buff_size = 1024*1024

            #set path for audio captures
            self.target_path = os.path.join(self.directory,'Captures')
            self._set_file_name()

        def _set_file_name(self):
            self.file = os.path.join(
                self.target_path,
                self.channel.name,
                str(self.today),
                "{}_{}T{}.mp3".format(
                    self.channel.name,
                    self.today,
                    self.start_time
                )
            )

        def capture(self):
            #create recording entity
            recording = Recording(self.channel.id, self.today, self.start_time, self.duration, self.file, 0)

            #start audio capturing
            try:
                self._write_stream_to_file(recording)
                # self._write_stream_till_tmr(recording)
                return recording
            except Exception as e:
                logging.error("Could not complete capturing, because an exception occured: {}".format(e))
                raise e


        def _write_stream_to_file(self, recording):
            not_ready = True
            logging.info("write {} \n to {}".format(
               self.channel.stream_url, recording.file
            ))

            try:
                dirname = os.path.dirname(recording.file)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)

                with open(recording.file, 'wb') as file:
                    stream = urlopen(self.channel.stream_url)
                    start_timestamp = time.mktime(time.localtime())
                    while not_ready:
                        try:
                            file.write(stream.read(self.buff_size))
                            if  time.time() - start_timestamp > recording.duration:
                                not_ready = False
                        except KeyboardInterrupt:
                            logging.warning("Capturing interupted.")
                            not_ready = False


                duration = time.time() - start_timestamp
                recording.duration = Helpers.get_time_from_sec(int(duration))
                recording.file_size = (os.path.getsize(recording.file) /1000000)
                recording.mimetype = 'audio/mpeg'
                recording.start_time = datetime.datetime.fromtimestamp(start_timestamp).strftime('%H:%M:%S')

                new_recording=( #is this necessary? there is already a recording
                            self.channel.id,
                            self.channel.name,
                            recording.date, #edit missing formation!!
                            recording.start_time,
                            recording.duration,
                            recording.file,
                            recording.file_size,
                            recording.is_episode)

                logging.debug("Finished recording: {}".format(new_recording))

                recording.id = self.db.create_recording(new_recording)
                return recording

            except UnicodeDecodeError as e:
                logging.error("Invalid input: {} ({})".format(e.reason, e.object[e.start:e.end]))
                # os.remove(recording.file)
                raise e

            except HTTPError as e:
                logging.error("Could not open URL {} ({:d}): {}".format(recording.channel.stream_url, e.code, e.msg))
                # os.remove(recording.file)
                raise e

            except IOError as e:
                logging.error("Could not write file {}: {}".format(recording.file, e))
                # os.remove(recording.file)
                raise e

            except socket.timeout as e:
                logging.warning("Capturing interupted. {}".format(e))
                raise e

            except Exception as e:
                logging.error("Could not capture show, because an exception occured: {}".format(e))
                # os.remove(recording.file)
                raise e

        def _write_stream_till_tmr(self, recording):
            not_ready = True
            logging.info("write {} \n to {}".format(
               self.channel.stream_url, recording.file
            ))

            try:
                dirname = os.path.dirname(recording.file)
                if not os.path.isdir(dirname):
                    os.makedirs(dirname)

                with open(recording.file, 'wb') as file:
                    stream = urlopen(self.channel.stream_url)
                    start_timestamp = time.mktime(time.localtime())
                    while not_ready:
                        try:
                            if self.today != datetime.date.today():
                                not_ready = False
                            file.write(stream.read(self.buff_size))
                        except KeyboardInterrupt:
                            logging.warning("Capturing interupted.")
                            not_ready = False


                duration = time.time() - start_timestamp
                recording.duration = Helpers.get_time_from_sec(int(duration))
                recording.file_size = (os.path.getsize(recording.file) /1000000)
                recording.mimetype = 'audio/mpeg'
                recording.start_time = datetime.datetime.fromtimestamp(start_timestamp).strftime('%H:%M:%S')

                new_recording=( #is this necessary? there is already a recording
                            self.channel.id,
                            self.channel.name,
                            recording.date, #edit missing formation!!
                            recording.start_time,
                            recording.duration,
                            recording.file,
                            recording.file_size,
                            recording.is_episode)

                recording.id = self.db.create_recording(new_recording)
                return recording

            except UnicodeDecodeError as e:
                logging.error("Invalid input: {} ({})".format(e.reason, e.object[e.start:e.end]))
                # os.remove(recording.file)
                raise e

            except HTTPError as e:
                logging.error("Could not open URL {} ({:d}): {}".format(recording.channel.stream_url, e.code, e.msg))
                # os.remove(recording.file)
                raise e

            except IOError as e:
                logging.error("Could not write file {}: {}".format(recording.file, e))
                # os.remove(recording.file)
                raise e

            except timeout as e:
                logging.warning("Capturing interupted. {}".format(e))
                raise e

            except Exception as e:
                logging.error("Could not capture show, because an exception occured: {}".format(e))
                # os.remove(recording.file)
                raise e
