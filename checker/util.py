
from pathlib import Path

import pandas as pd
import datetime

today = datetime.datetime.today()
delta = datetime.timedelta(days=1)

def fetch_sbd(tlim=(today-delta, today)):
    '''
    Function to fetch a list of profiles from the Argo Canada google drive, 
    including their metadata, for a given time period defined by either two
    delimiting datetimes, or a number of days ago and number of days from that
    time to be included.

    Args:
        tlim (tuple): tuple of two datestrings or datetimes used to select files
    
    Returns:
    '''

    return None

def get_last_profiles(index):
    '''
    Function that fetches the most recent profiles in a given argo index input,
    by checking for the highest cycle number for each unique WMO in the index.

    Args:
        index (pandas.DataFrame): 
    
    Returns:
        A reduced index containing only the information from the most recent
        cycle for each float
    '''

    # populate wmo column
    index['wmo'] = [f.split('/')[1] for f in index.file]

    keep_index = [(index[index.wmo == wmo].date == index[index.wmo == wmo].date.max()).index[0] for wmo in index.wmo]
    recent_profiles = index[keep_index]

    return recent_profiles

def expected_profiles(index, tlim=(today-delta, today)):
    '''
    Function that looks at the global Argo index for a given DAC (note - set
    up currently has MEDS as default, but could be adapted for any DAC), and
    given a float cycling period, returns a list of floats expected return
    a new profile within a specified date range. 

    Args: 
        tlim (tuple): tuple of two datestrings or datetimes used to select files
    
    Returns:
        list of floats (WMO numbers) expexted during the interval tlim
    '''

    return None
