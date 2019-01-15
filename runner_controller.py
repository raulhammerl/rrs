from datetime import timedelta, date
import subprocess
import os
import time

channels = ['WDR2', 'WDR3']
# , 'WDR4', 'BR_Heimat', 'Bayern+', 'Bayern_2_Sued', 'HR1',
# 'HR2', 'HR3', 'HR4', 'You_FM', 'MDR_Klassik', 'MDR_Jump', 'MDR_Sputnik', 'NDR_90.3',
# 'NDR2', 'NDR_Spez', 'NDR_Blue', 'NDR1', 'B888', 'Fritz', 'Radio_Eins', 'Br_Klassik',
# 'Bayern_1', 'Bayern_3']


# pool = multiprocessing.Pool(len(channels))

def parallel_starter():
    pass

def runner(directory):
    run_time = 1
    for channel in channels:
        # call = ['/usr/local/bin/python3', '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder/runner.py', channel, directory, str(time)]
        # file = channel+'-rec-log.txt'
        # log = os.path.join(directory, "Data", "Logs", file)
        # log = open(log, 'a')  # so that data written to it will be appended
        # c = subprocess.Popen(call, stdout=log, stderr=log)
        # exit_code = p.poll()
        run_channel(directory, channel)
        # while True:
        #     exit_code = run_channel(directory, channel)
        #     while exit_code == None:
        #         time.sleep(.10)
        #     print(exit_code, channel)
        #     exit_code = None


def run_channel(directory, channel):
    run_time = 1
    call = ['/usr/local/bin/python3', '/Users/Raul/Dropbox/Documents/Uni/Bachelorarbeit/AudioRecorder/runner.py', channel, directory, str(run_time)]
    file = channel+'-rec-log.txt'
    log = os.path.join(directory, "Data", "Logs", file)
    log = open(log, 'a')  # so that data written to it will be appended
    p = subprocess.Popen(call, stdout=log, stderr=log)
    exit_code = p.poll()
    while exit_code == None:
        time.sleep(.5)
        exit_code = p.poll()
    run_channel(directory, channel)


def main():
    # directory = '/Volumes/Untitled/Ba/'
    directory="Test"
    runner(directory)


if __name__ == "__main__":
    main()
