import json
import datetime as dt
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4
import time
from time import mktime
import csv
import pdb
from datetime import timezone
import smtplib
from email.message import EmailMessage
from asset_functions import create_clean_csv, write_to_csv, get_assets
from ifcb_helper import get_bins_in_range, get_datasets
import os
import pytz

def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time and the last time point on the Axiom THREDDS.
    This module gets the model data from THREDDS.
    call is of the form:
    timedelta=get_asset_delta(hfrID,hfrURL)
    Note: THREDDS can throw a number of errors and this code attemps to trap for some, but not all of these errors.
    '''
    now=dt.datetime.now(tz=dt.timezone.utc)
    try:
        radial_times=pd.read_csv(assetURL)
        lasttime=radial_times['time'].iloc[-1]
        # convert to usable time for comparison
        odate=dt.datetime.fromisoformat(lasttime.replace("Z","+00:00"))
    except Exception as e:
        timedelta_str="Error Number="+str(e.errno)+' '+str(e.strerror)
        return timedelta_str, assetURL
    time_delta=now-odate
    time_delta=now-odate
    days=time_delta.days
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    if days > 0:
        timedelta_str="{} days, {} hours, {} minutes".format(days,hours,minutes)
    elif hours > 0:
        timedelta_str="{} hours, {} minutes".format(hours,minutes)
    elif minutes > 0:
        timedelta_str="{} minutes".format(minutes)
    else:
        timedelta_str = "< 1 minute"
    return timedelta_str, assetURL
#
# main body of the code
#
if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/hfr_radial_timedelta.csv'
    create_clean_csv(outputfile,'hfrName',False)
    [hfrnames,assetID,radialURL]=get_assets('/home/flbahr/json_files/hfradar_radial_names.json')
    for i in np.arange(0,len(hfrnames)):
        timedelta_str,asseturl=get_asset_delta(assetID[i],radialURL[i])
        # need to trap for bad error type
        write_to_csv(asset_type='hfrName',asset=hfrnames[i],timedelta_str=timedelta_str,caloos_link=radialURL[i],outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/hfr_radial_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
