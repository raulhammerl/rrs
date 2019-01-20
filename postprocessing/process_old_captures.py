from datetime import timedelta, date
import subprocess

# channels = ['WDR2', 'Bayern_1', 'Bayern_3', 'B5_Aktuell', 'Puls', 'Br_Klassik', 'WDR4']
channels = ['B5_Aktuell', 'WDR2', 'WDR3', 'WDR4', 'BR_Heimat', 'Bayern+', 'Bayern_2_Sued', 'HR1',
'HR2', 'HR3', 'HR4', 'You_FM', 'MDR_Klassik', 'MDR_Jump', 'MDR_Sputnik', 'NDR_90.3',
'NDR2', 'NDR_Spez', 'NDR_Blue', 'NDR1', 'B888', 'Fritz', 'Radio_Eins', 'Br_Klassik',
'Bayern_1', 'Bayern_3']

def process_old_captures(directory, d1, d2):
    delta = d2 - d1

    for channel in channels:
        for i in range(delta.days + 1):
            d = d1 + timedelta(i)
            call = ['/usr/local/bin/python3', '/Users/kingkraul/rrs/digester.py', channel, directory, str(d)]
            subprocess.call(call)

def main():
    directory = '/Volumes/Untitled/BA/Alternative'
    month1 = 11
    month2 = 11
    day1 = 17
    day2 = 17
    d1 = date(2018, month1, day1)
    d2 = date(2018, month2, day2)
    process_old_captures(directory, d1,d2)


if __name__ == "__main__":
    main()
