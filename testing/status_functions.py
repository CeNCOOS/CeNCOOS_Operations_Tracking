import json
import datetime as dt
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4
import time
from time import mktime
import csv

def get_assets():
    ''' 
    Fetch asset names from the appropriate json file
    '''
    station_file='station_names.json'
    f=open(station_file)
    data=json.load(f)
    stationnames=[]
    stationID=[]
    stationURL=[]
    for i in data:
        stationnames.append(i['stationName'])
        stationID.append(i['datasetID'])
        stationURL.append(i['caloos_link'])
    f.close()
    #
    model_file='model_names.json'
    f=open(model_file)
    data=json.load(f)
    modelnames=[]
    modelID=[]
    modelURL=[]
    for i in data:
        modelnames.append(i['modelName'])
        modelID.append(i['datasetID'])
        modelURL.append(i['caloos_link'])
    f.close()
    #
    glider_file='glider_names.json'
    f=open(glider_file)
    data=json.load(f)
    glidernames=[]
    gliderID=[]
    gliderURL=[]
    gliderioosURL=[]
    for i in data:
        glidernames.append(i['gliderName'])
        gliderID.append(i['datasetID'])
        gliderURL.append(i['caloos_link'])
        gliderioosURL.append(i['ioos_link'])
    f.close()
    return [stationnames,stationID,stationURL,modelnames,modelID,modelURL,glidernames,gliderID,gliderURL,gliderioosURL]
def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom ERDDAP.
    '''
    now=dt.datetime.now(tz=dt.timezone.utc)
    # is the assetURL a THREDDS or ERDDAP URL?
    isthredds=assetURL.find('thredds')
    iserddap=assetURL.find('erddap')
    if isthredds > 0:
        # ----Model data----
        # issue with file access.  Had to use netCDF4 library to read
        asset_array=netCDF4.Dataset(assetURL)
        #
        try:
            asset_time=asset_array['time']
        else:
            asset_time=asset_array['ocean_time']
        except:
            print('Failure to find time variable\n')
        # Do we need offset or can code figure this out from the file
        units=asset_time.units
        ishours=units.find('hours')
        subunits=units.split()
        hascolon=subunits[-1].find(':')
        if hascolon > 0:
            yyyymmdd=subunits[-2]
            hhmmss=subunits[-1]
            bigt=yyyymmdd+'T'+hhmmss
            timeobj=time.strptime(bigt,"%Y-%m-%dT%H:%M:%S")

        else:
            yyyymmdd=subunits[-1]
            timeobj=time.strptime(yyyymmdd,"%Y-%m-%d")
        
        offset=dt.datetime.fromtimestamp(mktime(timeobj))
        if ishours >= 0:
            last_time=offset+dt.timedelta(hours=asset_time[-1])
        else:
            last_time=offset+dt.timedelta(seconds=asset_time[-1])
        time_delta=now-last_time

        # offset date is either at -1 or -2 if it has hours:minutes:seconds
        # C-HARM is hours since X (time) no hours:mintues:seconds
        # UCSC ROMS is hours since Y (time) time has hours:minutes:seconds
        # NEMURO is hours since W (time) time has hours:minutes:seconds
        # COAMPS is seconds since Z (time) time has hours:minutes:seconds
        # WCOFS is seconds since U (ocean_time) time has no hours:minutes:seconds
        # SFBOFS is hours since V (ocean_time) time has hours:minutes:seconds
    if iserddap > 0:
        # is it sensor data or glider data
        # need to define the URL etc to read from
        # is it a glider or shore station? how can we tell?  assetID and assetURL don't really help
        # shore station
        asset_df=pd.read_csv(f'https://erddap.cencoos.org/erddap/tabledap/{assetID}.csv?time')
        #asset_df=pd.read_csv(f'https://erddap.sensors.axds.co/erddap/tabledap/{erddapID}.csv?time')
        last_time = dt.datetime.strptime(df['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
        time_delta = now - last_time
       
   # parse for more meaningful output
    days = time_delta.days
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        timedelta_str = f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        timedelta_str = f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        timedelta_str = f"{minutes} minutes"
    else:
        timedelta_str = "< 1 minute"
    return timedelta_str

def create_clean_csv(outputfile):
    '''
    Create a CSV file with column headers
    '''
    with open(outputfile,'w',newline='') as csvfile:
        fieldnames=['Asset','timeDelta','caloosLink']
        write=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheater()

def write_to_csv(asset,timedelta_str,caloos_link,outputfile):
    '''
    Writes the timedelta string values for each asset as a new row in a CSV file.
    '''
    with open(outputfile,'a',newline='') as csvfile:
        fieldnames=['Asset','timeDelta','caloosLink']
        write=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow({'Asset':asset,'timeDelta':timedelta_str,'caloosLink':caloos_link})



# main body of code
if __name__=="__main__":
    outputfile='asset_timedelta.csv'
    create_clean_csv(outputfile=outputfile)
    [stationnames,stationID,stationURL,modelnames,modelID,modelURL,glidernames,gliderID,gliderURL,gliderioosURL]=get_assets()
    for i in np.arange(0,len(stationnames)):
        timedelta_str=get_asset_delta(stationID[i],stationURL[i])
        write_to_csv(asset=stationnames[i],timedelta_str=timedelta_str,caloos_link=stationURL[i],outputfile=outputfile)
    for i in np.arange(0,len(modelnames)):
        timedelta_str=get_asset_delta(modelID[i],modelURL[i])
        write_to_csv(asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=modelURL[i],outputfile=outputfile)
    for i in np.arange(0,len(glidernames)):
        timedelta_str=get_asset_delta(gliderID[i],gliderURL[i])
        write_to_csv(asset=glidernames[i],timedelta_str=timedelta_str,caloos_link=gliderURL[i],outputfile=outputfile)
    now=dt.datetime.now(tz=dt.timezone.utc)
    