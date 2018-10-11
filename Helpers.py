import datetime

def get_sec(time_str):
    if (isinstance(time_str, str) == False):
        print(time_str)
    else:
        if len(time_str) > 5:
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + int(s)
        else:
            h, m = time_str.split(':')
            return int(h) * 3600 + int(m) * 60

def get_sec_from_duration(time_str):
    if len(time_str) > 3:
        h, minutes = time_str.split('H')
        m, trash = minutes.split('M')
        return int(h) * 3600 + int (m) * 60
    elif('H' in time_str):
        h, trash = time_str.split('H')
        return int (h) * 3600
    else:
        m, trash = time_str.split('M')
        return int (m) * 60

def get_time_from_sec(time):
    s = time % 60
    m = time % 3600 // 60
    h = time // 3600
    return "{0:0=2d}".format(h) + ":" + "{0:0=2d}".format(m) + ":" + "{0:0=2d}".format(s)
