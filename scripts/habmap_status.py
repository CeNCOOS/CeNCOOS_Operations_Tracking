import json
import datetime as dt
import pandas as pd
import numpy as np
import netCDF4
import time
from time import mktime
import csv
import pdb
from datetime import timezone
import smtplib
#from email.message import EmailMessage
from ifcb_helper import get_bins_in_range, get_datasets
#from sfbofs_api_times import sfbofs_api_times
import os
from asset_functions import create_clean_csv, write_to_csv, get_assets
import gspread
from google.oauth2.service_account import Credentials
#
def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom ERDDAP.
    This module gets the CalHABMAP data for checking status of ingest of stations.
    Call is of the form:
    timedelta=get_asset_delta(habmapID, habmapURL)
    Note: habmap URLs point to scoos erddap server.
    '''
    iserddap=assetURL.find('erddap')    
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
    if iserddap > 0:
        # is it sensor data or glider data
        # need to define the URL etc to read from
        # is it a glider or shore station? how can we tell?  assetID and assetURL don't really help
        # shore station
        sccoos=assetURL.find('sccoos')
        if sccoos > 0:
            # this is for the HABMAP stations different ERDDAP
            asset_df=pd.read_csv('https://erddap.sccoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
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

def get_gspread_status(hab_file, hab_name):
    ''' 
    Fetch the status of the station from the Google Sheet
    https://docs.google.com/spreadsheets/d/1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ/edit?gid=0#gid=0
    '''
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("/home/flbahr/json_files/credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ"
    sheet = client.open_by_key(sheet_id)

    f = open(hab_file)
    data = json.load(f)
    x=sheet.worksheet('CalHABMAP').col_values(1)
    
    for station in data:
        try:
            sheet_location=x.index(station['stationName'])+1
        
            if station['stationName'] == glider_name:
                cell_value = sheet.worksheet('CalHABMAP').cell(sheet_location,2).value
                return cell_value
        except:
            pass
    # If through loop then just return
    return

if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/habmap_timedelta.csv'
    create_clean_csv(outputfile,'habName',True)
    [habnames,habID,habURL,erdURL]=get_assets('/home/flbahr/json_files/habmap_stations.json')
    for i in np.arange(0,len(habnames)):
        timedelta_str=get_asset_delta(habID[i],habURL[i])
        gsheet_status=get_gspread_status(hab_file='/home/flbahr/json_files/habmap_stations.json',hab_name=habnames[i])
        write_to_csv('habMAP',habnames[i],timedelta_str,erdURL[i],outputfile,gsheet_status)
    os.system('scp /home/flbahr/csv_output/habmap_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
 
