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
from datetime import timezone, timedelta
import smtplib
from email.message import EmailMessage
import os
import pytz
from asset_functions import create_clean_csv, write_to_csv, get_assets
#
def get_asset_delta(assetID,assetURL,caloosURL):
    '''
    Calculate the time delta between the present time and the last time point on the Axiom ERDDAP.
    This module gets the CDIP data for checking status of ingest of stations.
    Call is of the form:
    timedelta=get_asset_delta(cdipID, cdipURL,cdipcaloosURL)
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
        # Do not fail at this point, check to see if there is data at CDIP
        # Maybe we do want to return at this point as code won't show Axiom error if we continue...
    try:
        # This is the fallback to try and check if there is data not getting from CDIP to Axiom
        other_df=netCDF4.Dataset(assetURL)
        lastval=other_df['sstTime'][-1].data
        offset=dt.datetime(1970,1,1,0,0,0,0,pytz.UTC)
        last_time=offset+timedelta(seconds=lastval.item())
        time_delta = now - last_time    
       # parse for more meaningful output
        days = time_delta.days
        hours, remainder = divmod(time_delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        timedelta_str="Axiom error "+first_err+" CDIP times "
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
        timedelta_str='Axiom data error '+first_err+' CDIP error '+str(e)
        return timedelta_str

if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/cdip_timedelta.csv'
    create_clean_csv(outputfile,'CDIPName',False)
    [cdipnames,cdipID,cdipURL,cdipcaloosURL]=get_assets('/home/flbahr/json_files/CDIP.json')
    for i in np.arange(0,len(cdipnames)):
        timedelta_str=get_asset_delta(cdipID[i],cdipURL[i],cdipcaloosURL[i])
        theurl=cdipcaloosURL[i][:-8]+'html'
        write_to_csv(asset_type='CDIP',asset=cdipnames[i],timedelta_str=timedelta_str,caloos_link=theurl,outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/cdip_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
