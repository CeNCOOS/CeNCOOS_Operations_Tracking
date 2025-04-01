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
from ifcb_helper import get_bins_in_range, get_datasets
#from sfbofs_api_times import sfbofs_api_times
import os
from asset_functions import create_clean_csv, write_to_csv, get_assets

def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom ERDDAP.
    '''
    now=dt.datetime.now(tz=dt.timezone.utc)
    syear=str(now.year)
    nmon=now.month
    if nmon < 10:
        smon='0'+str(nmon)
    else:
        smon=str(nmon)
    nday=now.day
    if nday < 10:
        sday='0'+str(nday)
    else:
        sday=str(nday)
    iserddap=assetURL.find('erddap')    
    if iserddap > 0:
        # is it sensor data or glider data
        # need to define the URL etc to read from
        # is it a glider or shore station? how can we tell?  assetID and assetURL don't really help
        # shore station
        caloos=assetURL.find('caloos')
        cencoos=assetURL.find('cencoos')
        if (cencoos > 0) or (caloos > 0):
            try:
                #pdb.set_trace()
                asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
            except:
                try:
                    asset_df=pd.read_csv('https://gliders.ioos.us/erddap/tabledap/{}.csv?time'.format(assetID))
                except Exception as e:
                    timedetla_str='Error Number='+str(e.errno)+' '+str(e.strerror)
                    # failure to read time data from both Axiom and IOOS 
                    #timedelta_str='Error reading glider data from Axiom and IOOS'
                    return timedelta_str
        # was this a HTTP error or the wrong URL?
        last_time = dt.datetime.strptime(asset_df['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
        time_delta = now - last_time
       
   # parse for more meaningful output
    days = time_delta.days
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        timedelta_str="{} days, {} hours, {} minutes".format(days,hours,minutes)
        #timedelta_str = f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        timedelta_str="{} hours, {} minutes".format(hours,minutes)
        #timedelta_str = f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        timedelta_str="{} minutes".format(minutes)
        #timedelta_str = f"{minutes} minutes"
    else:
        timedelta_str = "< 1 minute"
    return timedelta_str
#
# main body of code
#
if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/glider_timedelta.csv'
    create_clean_csv(outputfile,'gliderName',False)
    [glidernames,gliderID,gliderioosURL,gliderURL]=get_assets('/home/flbahr/json_files/glider_names.json')
    for i in np.arange(0,len(glidernames)):
        timedelta_str=get_asset_delta(gliderID[i],gliderURL[i])
        urlout=gliderURL[i][:-3]+'graph'
        write_to_csv(asset_type='gliderName',asset=glidernames[i],timedelta_str=timedelta_str,caloos_link=urlout,outputfile=outputfile)
        #write_to_csv(asset_type='gliderName',asset=glidernames[i],timedelta_str=timedelta_str,caloos_link=gliderURL[i],outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/glider_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
