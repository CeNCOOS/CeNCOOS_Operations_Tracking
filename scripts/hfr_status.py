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
    # generate the URL to read
    theURL=assetURL
    #theURL=assetURL+'/'+assetID+'.ncd'
    #http://hfrnet-tds.ucsd.edu/thredds/dodsC/HFR/USWC/6km/hourly/RTV/HFRADAR_US_West_Coast_6km_Resolution_Hourly_RTV_best.ncd
    # try to trap for errors
    try:
        hfrdb=xr.open_dataset(theURL)
        lasttime=hfrdb['time'][-1]
    except Exception as e:
        timedelta_str='Error Number='+str(e.errno)+' '+str(e.strerror)
        return timedelta_str,assetURL
    # the units of last time are numpy.datetime64
    hfrlasttime=pd.Timestamp(lasttime.values)
    hfrlasttime=hfrlasttime.tz_localize('UTC')
    hfrlasttime=hfrlasttime.to_pydatetime()
    time_delta=now-hfrlasttime
    
    days = time_delta.days
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
# main body of code
#
if __name__=="__main__":
    outputfile='csv_output/hfradar_timedelta.csv'
    create_clean_csv(outputfile,'hfrName',False)
#    [hfrnames,hfrID,hfrURL]=get_assets('/home/flbahr/json_files/hfradar_names.json')
    [hfrnames,hfrID,ioosURL,hfrURL]=get_assets('json_files/hfradar_names_update.json')
    for i in np.arange(0,len(hfrnames)):
        timedelta_str,asseturl=get_asset_delta(hfrID[i],hfrURL[i])
        write_to_csv(asset_type='hfrName',asset=hfrnames[i],timedelta_str=timedelta_str,caloos_link=ioosURL[i],outputfile=outputfile)
    #os.system('scp /home/flbahr/csv_output/hfradar_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
