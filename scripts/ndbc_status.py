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
import os
from asset_functions import create_clean_csv, write_to_csv, get_assets
import urllib
import pytz
def get_asset_delta(assetID,assetURL,caloosURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom ERDDAP.
    This module gets the NDBC data for checking status of ingest of stations.
    Call is of the form:
    timedelta=get_asset_delta(ndbcID, ndbcURL,ndbccaloosURL)
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
    try:
        asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
        last_time = dt.datetime.strptime(asset_df['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
        time_delta = now - last_time    
       # parse for more meaningful output
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
        return timedelta_str
    except Exception as e:
        # This is the error getting data from Axiom
        first_err='Error Number='+str(e.errno)+' '+str(e.strerror)
        timedelta_str=first_err
        return timedelta_str
        # Do not fail at this point, check to see if there is data at NDBC
        # Maybe we do want to return at this point as code won't show Axiom error if we continue...
    try:
        # This is the fallback to try and check if there is data not getting from CDIP to Axiom
        data=urllib.request.urlopen(assetURL).read().decode('utf-8')
        lines=data.split('\n')
        # most recent data in files is at the top
        recentdata=lines[2] # first 2 lines are header lines
        values=recentdata.split(' ')
        last_time=dt.datetime(int(values[0]),int(values[1]),int(values[2]),int(values[3]),int(values[4]),int(values[5]),0,pytz.UTC)
        time_delta = now - last_time    
       # parse for more meaningful output
        days = time_delta.days
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        timedelta_str="Axiom error "+first_err+" NDBC times "
        if days > 0:
            timedelta_str=timedelta_str+"{} days, {} hours, {} minutes".format(days,hours,minutes)
        elif hours > 0:
            timedelta_str=timedleta_str+"{} hours, {} minutes".format(hours,minutes)
        elif minutes > 0:
            timedelta_str=timedelta_str+"{} minutes".format(minutes)
        else:
            timedelta_str =timedelta_str+ "< 1 minute"
        return timedelta_str       
    except Exception as e:
        # This is the ultimate failure as an error at both
        timedelta_str='Axiom data error '+first_err+' NDBC error '+str(e)
        return timedelta_str



if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/ndbc_timedelta.csv'
    create_clean_csv(outputfile,'ndbcName',False)
    [ndbcnames,ndbcID,ndbcURL,ndbccaloosURL]=get_assets('/home/flbahr/json_files/NDBC.json')
    for i in np.arange(0,len(ndbcnames)):
        #print(ndbcnames[i])
        timedelta_str=get_asset_delta(ndbcID[i],ndbcURL[i],ndbccaloosURL[i])
        #print(timedelta_str)
        theurl=ndbccaloosURL[i][:-8]+'html'
        write_to_csv(asset_type='NDBC',asset=ndbcnames[i],timedelta_str=timedelta_str,caloos_link=theurl,outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/ndbc_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
