
from pathlib import Path

import pandas as pd
import datetime

today = datetime.datetime.today()
delta = datetime.datetime.timedelta(days=1)

def fetch_sbd(tlim=(today-delta, today), days_ago=None, ndays=None):
    '''
    Function to fetch a list of profiles from the Argo Canada google drive, 
    including their metadata, for a given time period defined by either two
    delimiting datetimes, or a number of days ago and number of days from that
    time to be included.

    Args:
        - tlim (tuple): tuple of two datestrings or datetimes used to select files
        - days_ago (float): number of days ago to get files, can be float
        - ndays (float): number of days from `days_ago` to get files
    
    Returns:
    '''


    return None

def expected_profiles(tlim=(today-delta, today), days_ago=None, ndays=None):
    '''
    Function that looks at the global Argo index for a given DAC (note - set
    up currently has MEDS as default, but could be adapted for any DAC), and
    given a float cycling period, returns a list of floats expected return
    a new profile within a specified date range. 

    Args: 
    '''

    return None
