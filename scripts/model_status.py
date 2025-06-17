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
#import smtplib
#from email.message import EmailMessage
from asset_functions import create_clean_csv, write_to_csv, get_assets
#from ifcb_helper import get_bins_in_range, get_datasets
#from ifcb_helper import get_bins_in_range, get_datasets
#from sfbofs_api_times import sfbofs_api_times
import os
import gspread
from google.oauth2.service_account import Credentials
import gspread
from google.oauth2.service_account import Credentials

def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time and the last time point on the Axiom THREDDS.
    This module gets the model data from THREDDS.
    call is of the form:
    timedelta=get_asset_delta(modelID,modelURL)
    Note: THREDDS can throw a number of errors and this code attemps to trap for some, but not all of these errors.
    Each model has a slightly diffrent call form for the THREDDS server and slightly different responses.
    That is why the code is not as clean as hoped.
    '''
    now=dt.datetime.now(tz=dt.timezone.utc)
    # the UCSC ROMS for 3/14 latest value is 3/12
    if assetID=='UCSC':
        now=now-dt.timedelta(days=4)    
    syear=str(now.year)
    nmon=now.month
    if nmon < 10:
        smon='0'+str(nmon)
    else:
        smon=str(nmon)
    nday=now.day
    now=dt.datetime.now(tz=dt.timezone.utc) # re get now to deal with offset for UCSC ROMS above
    # it appears that the model output for at UCSC is slow by 2 days
    if nday < 10:
        sday='0'+str(nday)
    else:
        sday=str(nday)
    # Model asset access is only by thredds at this time
    isthredds=assetURL.find('thredds')
    if isthredds > 0:
        # ----Model data----
        # issue with file access.  Had to use netCDF4 library to read
        # need to trap for network/data access errors
        # if UCSC ROMS need to add YYYY and YYYY_MM etc to name
        if assetID=='UCSC':
            # sample url call is the following
            #http://thredds.cencoos.org/thredds/dodsC/cencoos/ccsnrt/2024/2024_09/ccsnrt_2024_09_05.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/ccsnrt_'+syear+'_'+smon+'_'+sday+'.nc'
            #print(assetURL)
        if assetID=='NOAA_OFS_SFBOFS':
            # sample url call
            #http://thredds.cencoos.org/thredds/dodsC/noaa/coops/ofs/aws_sfbofs_regulargrid/2024/2024_10/sfbofs_2024-10-16.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/sfbofs_'+syear+'-'+smon+'-'+sday+'.nc'
        if assetID=='AWS_WCOFS':
            # sample url call
            #http://thredds.cencoos.org/thredds/dodsC/noaa/coops/ofs/aws_wcofs/2024/2024_10/wcofs_2024-10-17.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/wcofs_'+syear+'-'+smon+'-'+sday+'.nc'
            #print(assetURL)
        # There have been error issues when reading from thredds servers.  This code attempts to trap and catch
        # any errors.
        try:
            asset_array=netCDF4.Dataset('[FillMismatch]'+assetURL)
        except Exception as e:
            # trap for any error opening the dataset
            timedelta_str='Error Number='+str(e.errno)+' '+str(e.strerror)
            return timedelta_str,assetURL
        try:
            asset_time=asset_array['time']
        except IndexError:
            asset_time=asset_array['ocean_time']
        except:
            # could not read either values that should be available for time in the dataset
            timedelta_str="Could not find time in the dataset"
            return timedelta_str, assetURL
        # Do we need offset or can code figure this out from the file
        units=asset_time.units
        ishours=units.find('hours')
        subunits=units.split()
        hascolon=subunits[-1].find(':')
        # check format for the date in the file and parse accordingly.
        if hascolon > 0:
            yyyymmdd=subunits[-2]
            hhmmss=subunits[-1]
            bigt=yyyymmdd+'T'+hhmmss
            timeobj=time.strptime(bigt,"%Y-%m-%dT%H:%M:%S")

        else:
            yyyymmdd=subunits[-1]
            timeobj=time.strptime(yyyymmdd,"%Y-%m-%d")
        
        offset=dt.datetime.fromtimestamp(mktime(timeobj))
        # check for RuntimeError
        try:
            asset_time[-1]
        except RuntimeError as err:
            # There was an error accessing the time variable itself in the dataset
            timedelta_str='"RuntimeError accessing last time element "'+str(err)+'"'
            return timedelta_str, assetURL
        if ishours >= 0:
            last_time=offset+dt.timedelta(hours=int(asset_time[-1]))
        else:
            last_time=offset+dt.timedelta(seconds=int(asset_time[-1]))
        time_delta=now-last_time.replace(tzinfo=dt.timezone.utc)
        # NOTES on time in the file.
        # offset date is either at -1 or -2 if it has hours:minutes:seconds
        # C-HARM is hours since X (time) no hours:mintues:seconds
        # UCSC ROMS is hours since Y (time) time has hours:minutes:seconds
        # NEMURO is hours since W (time) time has hours:minutes:seconds
        # COAMPS is seconds since Z (time) time has hours:minutes:seconds
        # WCOFS is seconds since U (ocean_time) time has no hours:minutes:seconds
        # SFBOFS is hours since V (ocean_time) time has hours:minutes:seconds
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
    return timedelta_str, assetURL
#
def get_gspread_status(model_file,model_name):
    scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("gsheet/credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ"
    sheet = client.open_by_key(sheet_id)

    f = open(model_file)
    data = json.load(f)
    x=sheet.worksheet('Models').col_values(1)
    for station in data:
        try:
            sheet_location=x.index(station['modelName'])+1
        
            if station['modelName'] == model_name:
                cell_value = sheet.worksheet('Models').cell(sheet_location,2).value
                return cell_value
        except:
            pass
    # If through loop then just return
    return

#
# main body of code
#
if __name__=="__main__":
    outputfile='csv_output/model_timedelta.csv'
    #create_clean_csv(outputfile,'modelName',False)
    create_clean_csv(outputfile,'modelName',True)
    [modelnames,modelID,modelURL,catURL]=get_assets('json_files/model_names.json')
    for i in np.arange(0,len(modelnames)):
        timedelta_str,asseturl=get_asset_delta(modelID[i],modelURL[i])
        gsheet_status=get_gspread_status(model_file='json_files/model_names.json',model_name=modelnames[i])         		
        #write_to_csv(asset_type='modelName',asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=modelURL[i],outputfile=outputfile)
        #pdb.set_trace()
        write_to_csv('modelName',modelnames[i],timedelta_str,catURL[i],outputfile,gsheet_status)
        #write_to_csv(asset_type='modelName',asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=catURL[i],outputfile=outputfile)
        #pdb.set_trace()
        #write_to_csv('modelName',modelnames[i],timedelta_str,catURL[i],outputfile,gsheet_status)
        #write_to_csv(asset_type='modelName',asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=catURL[i],outputfile=outputfile)
        #write_to_csv(asset_type='modelName',asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=asseturl+'.html',outputfile=outputfile)
    #os.system('scp csv_output/model_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
