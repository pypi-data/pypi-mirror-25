from datetime import (
    datetime,
    timedelta
)


def seconds_to_dhms(seconds):
    '''converts seconds to dhms format'''
    sec = timedelta(seconds=seconds)
    seconds = datetime(1, 1, 1) + sec
    return '{}:{}:{}:{}'.format(seconds.day - 1, seconds.hour, seconds.minute, seconds.second)


def unsafe_float_conversion(string):
    '''tries to convert a string to float, and returns 0.0 if it can't'''
    try:
        return float(string)
    except ValueError:
        try:
            return float(int(string))
        except ValueError:
            return 0.0


def date_to_str(date, short=False, offset=0):
    '''converts date to string'''
    if type(date) == int:
        date = datetime.fromtimestamp(date)
    date = date + timedelta(hours=offset)
    if short:
        return datetime.strftime(date, '%Y-%m-%d')
    else:
        return datetime.strftime(date, '%Y-%m-%d %H:%M:%S')


def ts_to_str(ts):
    '''converts a timestamp to string'''
    return datetime.utcfromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')
