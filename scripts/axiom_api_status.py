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
import requests
import os
def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time and the last time point on the Axiom API.
    call is of the form:
    timedelta=get_asset_delta(datasetID,apiURL)
    This code uses the requests module to check on status
    '''
    # get present time
    now=dt.datetime.now(tz=dt.timezone.utc)
    # make the request
    sfbr=requests.get(assetURL)
# check status code
    status_code=sfbr.status_code
    if status_code==200:
        times=sfbr.text
        thetimes=times.split(',')
        lasttime=thetimes[-1][1:-2]
        odate=dt.datetime.fromisoformat(lasttime.replace("Z","+00:00"))
        #odate=dt.datetime.strptime(lasttime,'%Y-%m-%dT%H:%M:%SZ')
    else:
        # return the error string since we want to know we got a http error
        timedelta_str="Received HTTPS status error "+str(status_code)
        return timedelta_str, assetURL
    time_delta=now-odate
    days=time_delta.days
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    # Due to these being forecast times we can have negative times
    neg=0
    if days < 0:
        timedelta_str="{} days, {} hours, {} minutes".format(days,hours,minutes)
        neg=1
    elif hours < 0:
        timedelta_str="{} hours, {} minutes".format(hours,minutes)
        neg=1
    elif minutes < 0:
        timedelta_str="{} minutes".format(minutes)
        neg=1
    # use a flag to check if any of the above have happened and return otherwise get the positive time.
    if neg==1:
        return timedelta_str,assetURL
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
    outputfile='/home/flbahr/csv_output/api_timedelta.csv'
    create_clean_csv(outputfile,'apiName',False)
    [apinames,assetID,caloosURL,apiURL]=get_assets('/home/flbahr/json_files/api_url.json')
    for i in np.arange(0,len(apinames)):
        timedelta_str,asseturl=get_asset_delta(assetID[i],apiURL[i])
        # need to trap for bad error type
        write_to_csv(asset_type='apiName',asset=apinames[i],timedelta_str=timedelta_str,caloos_link=caloosURL[i],outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/model_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
    
    
