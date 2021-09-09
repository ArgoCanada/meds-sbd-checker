
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


def get_next_profiles(index, cycle_time):
    '''
    Function that will take each profile in a given index and give the date
    of the next cycle given a cycle time in hours. The cycle_time argument
    is mandatory as some floats may operatate on different time periods to
    accomplish different goals (see Johnson & Bif 2021), however a 10-day
    period (240 hours) is typical. 

    Args:
        index (pandas.DataFrame): subset of the Argo global index
        cycle_time (float): period in hours of the cycle time, typically
        10 days (240 hours)

    Returns:
        Original index with an extra column for next profile date
    '''

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
