from datetime import timedelta, date
from subprocess import call

channels = ['WDR2', 'Bayern_1', 'Bayern_3', 'B5_Aktuell', 'Puls', 'Br_Klassik', 'WDR4']

def process_old_captures(d1, d2):
    delta = d2 - d1

    for channel in channels:
        for i in range(delta.days + 1):
            d = d1 + timedelta(i)
            call = ['/usr/local/bin/python3', '/Users/Raul/rrs/digesting_runner.py', channel, directory, d]
            call(call)

def main():
    directory = '/Volumes/Ba/'
    month = 10
    day1 = 20
    day2 = 30
    d1 = date(2018, month, day1)
    d2 = date(2018, month, day2)
    process_old_captures(d1,d2)


if __name__ == "__main__":
    main()
