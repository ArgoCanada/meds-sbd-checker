
from pathlib import Path

import numpy as np
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

def parse_dates(index):
    '''
    Function to parse dates in the Argo global index. It is not recommended to
    perform this operation on the entire index.

    Args:
        index (pandas.DataFrame): Argo global, bio, or synthetic index
    
    Returns:
        A copy of the index where the column "date" has been populated with
        python datetime.datetime objects rather than large integer dates
    '''

    ### argopandas does this already

def last_profiles(index, n=1):
    '''
    Function that fetches the most recent profiles in a given argo index input,
    by checking for the highest cycle number for each unique WMO in the index.

    Args:
        index (pandas.DataFrame): Argo global, bio, or synthetic index
        n (int, optional): number of recent profiles for each float to get
    
    Returns:
        A reduced index containing only the information from the most recent
        cycle for each float
    '''

    # populate wmo column
    index['wmo'] = [f.split('/')[1] for f in index.file]
    index_copy = index[:]

    keep_index = []
    for i in range(n):
        keep_index = keep_index + [(index[index.wmo == wmo].date == index[index.wmo == wmo].date.max()).index[0] for wmo in index.wmo]
        index = index[~keep_index]
    recent_profiles = index_copy[keep_index]

    return recent_profiles


def next_profiles(index, cycle_time):
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

    if not isinstance(index.date.iloc[0], datetime.datetime):
        raise ValueError('Index column "date" is not type datetime.datetime, please use function parse_dates() or load index using argopandas')

    delta = datetime.timedelta(hours=cycle_time)
    next_index = index[:]
    next_index['next_profile'] = next_index['date'] + delta

    return next_index

def expected_profiles(index, tlim=(today-delta, today)):
    '''
    Function that looks at the global Argo index for a given DAC (note - set
    up currently has MEDS as default, but could be adapted for any DAC), and
    given a float cycling period, returns a list of floats expected return
    a new profile within a specified date range. 

    Args: 
        tlim (tuple): tuple of two datestrings or datetimes used to select files
    
    Returns:
        list of floats (WMO numbers) expected during the interval tlim
    '''

    if 'next_profile' not in index.columns:
        index = next_profiles(index)

    tlim_index = np.logical_and(index.date > tlim[0], index.date < tlim[1])
    expected_profiles

    return None
