import logging
import os
import subprocess

import Database
import Helpers



class AudioDataHandler:

    def __init__(self, directory, date, channel_name):
        self.db = Database.Database(directory)
        self.date = date
        self.channel = self.db.find_channel_by_name(channel_name)


    def extract_episode(self, episode, recording):
        time_frame_tpl = self._calculate_time_frame(episode, recording)

        if time_frame_tpl is not None:
            start_time = time_frame_tpl[0]
            end_time = time_frame_tpl[1]
            extracted_episode = self._extract_file(episode, recording, start_time, end_time)
            return extracted_episode

        else:
            return

    def _set_file_name(self, episode, recording):
        file_name = recording.file[:-12].replace("/Captures", "/Extracts") \
                    + str(episode.start_time).replace(":", "-") + "_show" \
                    + str(episode.show_id) + ".mp3"
        return file_name


    def _extract_file(self, episode, recording, start_time, end_time):
        output_file = self._set_file_name(episode, recording)
        logging.debug("extracting episode to: {}".format(output_file))
        recording.duration = end_time-start_time
        if os.path.isfile(output_file):
            logging.debug("file already extracted")
            return output_file
        else:
            try:
                #format entity for db
                new_recording=(
                    recording.channel_id,
                    recording.channel_name,
                    str(recording.date),
                    str(recording.start_time),
                    recording.duration,
                    # recording.file,
                    # recording.file_size,
                    # recording.is_episode,
                    output_file,
                    0, # file_size
                    1 # is_episode
                )

                # save entity in db
                recording.id = self.db.create_recording(new_recording)
                self.db.update_episode_recording(episode.id, recording.id)

                Helpers.create_dir(output_file)

                # extract episode from file
                call = ['/usr/local/bin/ffmpeg','-y',
                        '-i', recording.file ,
                        '-ss', str(start_time) ,'-to', str(end_time),
                        '-c' ,'copy',
                         '-metadata', 'album={}'.format(episode.show_id),
                         '-metadata', 'track={}'.format(recording.id),
                         '-metadata', 'artist={}'.format(self.channel.id),
                         output_file]
                subprocess.call(call)
                return output_file

            except Exception as e:
                logging.error(e)
                raise e

    def _calculate_time_frame(self, episode, recording):
        """calcute time frames where to cut episode extract"""

        recording_start_time = Helpers.get_sec(recording.start_time)
        recording_end_time = Helpers.get_sec(recording.duration) + recording_start_time

        episode_start_time = Helpers.get_sec(episode.start_time)
        episode_end_time = Helpers.get_sec_from_duration(episode.duration) + episode_start_time

        logging.debug ("recording start time {}".format(recording_start_time))
        logging.debug ("episode start time {}".format(episode_start_time))

        logging.debug("recording end time {}".format(recording_end_time))
        logging.debug("episode end time {}".format(episode_end_time))

        # check if episodes ended before recordings starts
        if episode_end_time < recording_start_time:
            logging.debug("episode not in time frame")
            return #continue

        if recording.channel_id != self.channel.id:
            logging.debug("episode from another channel")
            return #continue

        # check if episode started afer recordings ends
        if episode_start_time > recording_end_time:
            logging.debug("all episodes for time frame checked")
            return #break

        # check if episode started after recording
        if episode_start_time > recording_start_time:
            start_time = episode_start_time - recording_start_time
            recording.start_time = episode_start_time

        # check if recording started after the episode started
        elif episode_start_time < recording_start_time:
            start_time = 0

        # cut episode to an hour max for efficiency reasons
        if (episode_end_time - start_time) > 3600:
            end_time = start_time + 3600

        # check if episode ended before recording
        elif episode_end_time < recording_end_time:
            end_time = episode_end_time - recording_start_time

        # check if episode ended afer recording
        elif episode_end_time > recording_end_time:
            end_time = Helpers.get_sec(recording.duration)

        logging.debug ("start time in sec {}".format(start_time))
        logging.debug("end time {}".format(end_time))
        logging.debug("file{}".format(recording.file))

        return (start_time, end_time)
