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
#import smtplib
#from email.message import EmailMessage
from ifcb_helper import get_bins_in_range, get_datasets
#from sfbofs_api_times import sfbofs_api_times
import os
from asset_functions import create_clean_csv, write_to_csv, get_assets
import gspread
from google.oauth2.service_account import Credentials

def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom IFCB dashboard.
    Note this code makes use of some functions to get bins and data sets from the IFCB dashboard.
    The instrument does not provide a straight forward access to the last time-point obtained.
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
        # can't just do the above since IFCB dashboard doesn't operate in the same way....
    now=dt.datetime.now()
    # lets not limit to yesterday and look 2 months back?
    yesterday=now+dt.timedelta(days=-60)
    start=str(yesterday.year)+'-'+str(yesterday.month)+'-'+str(yesterday.day)
    stop=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
    samples=get_bins_in_range(start,stop,assetID,'https://ifcb.caloos.org')
    #pdb.set_trace()
    try:
        lastfile=samples.iloc[-1]
        underscore=lastfile.find('_')
        lastfile=lastfile[0:underscore]
        dtobj=dt.datetime.strptime(lastfile,'D%Y%m%dT%H%M%S')
        time_delta=now-dtobj
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
    except:
        timedelta_str='No data within the last 60 days'
        #timedelta_str=samples
    return timedelta_str

def get_gspread_status(ifcb_file, ifcb_name):
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

    f = open(ifcb_file)
    data = json.load(f)
    x=sheet.worksheet('IFCB').col_values(1)
    
    for station in data:
        try:
            sheet_location=x.index(station['IFCBName'])+1
        
            if station['IFCBName'] == ifcb_name:
                cell_value = sheet.worksheet('IFCB').cell(sheet_location,2).value
                return cell_value
        except:
            pass
    # If through loop then just return
    return

    
if __name__=="__main__":
    outputfile='/home/flbahr/csv_output/ifcb_timedelta.csv'
    create_clean_csv(outputfile,'ifcbName',True)
    [ifcbnames,ifcbID,ifcbURL]=get_assets('/home/flbahr/json_files/ifcb_names.json')
    for i in np.arange(0,len(ifcbnames)):
        timedelta_str=get_asset_delta(ifcbID[i],ifcbURL[i])
        gsheet_status=get_gspread_status(ifcb_file='/home/flbahr/json_files/ifcb_names.json',ifcb_name=ifcbnames[i])
        write_to_csv('ifcbName',ifcbnames[i],timedelta_str,ifcbURL[i],outputfile,gsheet_status)
        #write_to_csv(asset_type='ifcbName',asset=ifcbnames[i],timedelta_str=timedelta_str,caloos_link=ifcbURL[i],outputfile=outputfile)
    os.system('scp /home/flbahr/csv_output/ifcb_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
