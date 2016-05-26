from datetime import datetime


def generate_filename(base='track_times', timestamp_format=None):
    """
    Create a unique filename that incorporates a timestamp. 
    
    For example if the filename were generated on the 19th of April 2016
    at 12:16:47, then the default output would be: "track_times_2016-04-19_1216.csv"
    
    Parameters
    ----------
    base: str
        The base name for the filename, a timestamp is appended to this.
    timestamp_format: str
        A strftime formatting string. See "http://strfti.me/" for more
        details.
        
    Returns
    -------
    str
        A unique filename.
    """
    if timestamp_format is None:
        timestamp_format = '%Y-%m-%d_%H%M'
    time_stamp = datetime.now().strftime(timestamp_format)

    name = '{}_{}.csv'.format(base, time_stamp)
    if '/' in name:
        raise ValueError('Invalid filename: {}'.format(name))

    return name

def human_readable(millis): 
    """ 
    Take a number of milliseconds and turn it into a string with the format
    "min:sec.millis".
    """
    if not isinstance(millis, int):
        raise TypeError('millis must be a positive integer')

    if millis < 0:
        raise ValueError('millis must be a positive integer')

    seconds, ms = divmod(millis, 1000)
    minutes, seconds = divmod(seconds, 60)

    return '{}:{}.{}'.format(minutes, seconds, int(ms))
    
