# from pydub import AudioSegment
import logging
import os
import subprocess
import Database
import Helpers



logging.basicConfig(level=logging.DEBUG)

class Audio_data_handler:

    def __init__(self, db_file, date, channel):
        self.db = Database.Database(db_file)
        self.date = date
        self.channel = channel


    def cut_blob_into_episodes(self):
        # find all episodes from date
        all_rows = self.db.find_episodes_by_date(self.date)
        logging.debug("trying to find episodes with date: {}".format(self.date))
        for episode in all_rows:
            #get episode attributes
            episode_id = episode[0]
            logging.debug("found episode with id: {}".format(episode_id))
            episode = self.db.find_episode_by_id(episode_id)

            # find corresponding recording
            recording = self.db.find_recording(episode.recording_id)
            logging.debug("Recording found: {}". format(recording))

            # check if recording is already an extract if so skip episode
            if recording.is_episode is 1:
                logging.debug("recording is already an episode")
                continue

            #calcute time frames to cut
            recording_start_time = Helpers.get_sec(recording.start_time)
            episode_start_time = Helpers.get_sec(episode.start_time)
            episode_end_time = Helpers.get_sec_from_duration(episode.duration) + episode_start_time
            recording_end_time = Helpers.get_sec(recording.duration) + recording_start_time

            # TODO check for double entries
            logging.debug ("recording start time {}".format(recording_start_time))
            logging.debug ("episode start time {}".format(episode_start_time))

            logging.debug("recording end time {}" .format(recording_end_time))
            logging.debug("episode end time {}" .format(episode_end_time))

            # check if episodes ended before recordings starts
            if episode_end_time < recording_start_time:
                logging.debug("episode not in time frame")
                continue

            if recording.channel_id != self.channel.id:
                logging.debug("episode from another channel")
                continue

            # check if episode started afer recordings ends
            if episode_start_time > recording_end_time:
                logging.debug("all episodes for time frame checked")
                break

            # check if episode started after recording
            if episode_start_time > recording_start_time:
                start_time = episode_start_time - recording_start_time
                recording.start_time = Helpers.get_time_from_sec(episode_start_time)

            # check if recording started after the episode started
            elif episode_start_time < recording_start_time:
                start_time = 0 #Helpers.get_sec(recording.start_time)

            # check if episode ended before recording
            if episode_end_time < recording_end_time:
                end_time = episode_end_time - recording_start_time

            # check if episode ended afer recording
            elif episode_end_time > recording_end_time:
                end_time = Helpers.get_sec(recording.duration)

            logging.info ("start time in sec {}".format(start_time))
            logging.info("end time {}" .format(end_time))
            logging.info("file{}".format(recording.file))

            # set file name
            outputstr = recording.file[:-12] + str(episode.start_time).replace(":", "-") + "_show" + str(episode.show_id) + ".mp3"

            try:
                # extract episode from file
                call = ['ffmpeg', '-i' , recording.file ,
                        '-ss', str(start_time) ,'-to', str(end_time),
                        '-c' ,'copy',
                         '-metadata', 'album={}'.format(episode.show_id),
                         '-metadata', 'track={}'.format(recording.id),
                         '-metadata', 'artist={}'.format(self.channel.id),
                         outputstr]
                subprocess.call(call)

                # create new recording entity
                recording.file = outputstr
                recording.is_episode = 1
                recording.duration = Helpers.get_time_from_sec(episode_end_time - episode_start_time)

                #format entity for db
                new_recording=(
                    recording.channel_id,
                    recording.channel_name,
                    str(recording.date), #edit missing formation!!
                    str(recording.start_time),
                    recording.duration,
                    recording.file,
                    recording.file_size,
                    recording.is_episode
                )

                # save entity in db
                recording.id = self.db.create_recording(new_recording)
                self.db.update_episode_recording(episode_id, recording.id)

            except Exception as e:
                logging.error(e)
                raise e
