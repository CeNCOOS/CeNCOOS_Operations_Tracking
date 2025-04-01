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

def get_assets():
    ''' 
    Fetch asset names from the appropriate json file
    '''
    station_file='/home/flbahr/json_files/station_names.json'
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
    model_file='/home/flbahr/json_files/model_names.json'
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
    glider_file='/home/flbahr/json_files/glider_names.json'
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
    #
    ifcb_file='/home/flbahr/json_files/ifcb_names.json'
    f=open(ifcb_file)
    data=json.load(f)
    ifcbnames=[]
    ifcbID=[]
    ifcbURL=[]
    for i in data:
        ifcbnames.append(i['IFCBName'])
        ifcbID.append(i['datasetID'])
        ifcbURL.append(i['caloos_link'])
    f.close()
    #
    hab_file='/home/flbahr/json_files/habmap_stations.json'
    f=open(hab_file)
    data=json.load(f)
    habnames=[]
    habID=[]
    habURL=[]
    for i in data:
        habnames.append(i['stationName'])
        habID.append(i['datasetID'])
        habURL.append(i['caloos_link'])
    f.close()
   
    
    return [stationnames,stationID,stationURL,modelnames,modelID,modelURL,glidernames,gliderID,gliderURL,gliderioosURL,ifcbnames,ifcbID,ifcbURL,habnames,habID,habURL]
def get_asset_delta(assetID,assetURL):
    '''
    Calculate the time delta between the present time nad the last time point on the Axiom ERDDAP.
    '''
    now=dt.datetime.now(tz=dt.timezone.utc)
    # is the assetURL a THREDDS or ERDDAP URL?
    isthredds=assetURL.find('thredds')
    iserddap=assetURL.find('erddap')
    isstation=assetURL.find('station')
    if isthredds > 0:
        # ----Model data----
        # issue with file access.  Had to use netCDF4 library to read
        # need to trap for network/data access errors
        # if UCSC ROMS need to add YYYY and YYYY_MM etc to name
        if assetID=='UCSC':
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
#http://thredds.cencoos.org/thredds/dodsC/cencoos/ccsnrt/2024/2024_09/ccsnrt_2024_09_05.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/ccsnrt_'+syear+'_'+smon+'_'+sday+'.nc'
            print(assetURL)
            #pdb.set_trace()
        #
        if assetID=='NOAA_OFS_SFBOFS':
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
#http://thredds.cencoos.org/thredds/dodsC/noaa/coops/ofs/aws_sfbofs_regulargrid/2024/2024_10/sfbofs_2024-10-16.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/sfbofs_'+syear+'-'+smon+'-'+sday+'.nc'
        if assetID=='AWS_WCOFS':
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
#http://thredds.cencoos.org/thredds/dodsC/noaa/coops/ofs/aws_wcofs/2024/2024_10/wcofs_2024-10-17.nc
            assetURL=assetURL+syear+'/'+syear+'_'+smon+'/wcofs_'+syear+'-'+smon+'-'+sday+'.nc'
            print(assetURL)
        try:
            asset_array=netCDF4.Dataset('[FillMismatch]'+assetURL)
#        except Exception as ex:
#            print(ex)
        except:
            # trap for any error opening the dataset 
            timedelta_str='NetCDF4 read error with dataset'
            return timedelta_str
        try:
            asset_time=asset_array['time']
        except IndexError:
            asset_time=asset_array['ocean_time']
        except:
            # could not read either values that should be available for time in the dataset
            timedelta_str='Could not find time in the dataset'
            return timedelta_str
#            print('Failure to find time variable\n')
        # Do we need offset or can code figure this out from the file
        units=asset_time.units
        ishours=units.find('hours')
        subunits=units.split()
        hascolon=subunits[-1].find(':')
        #if assetID=='UCSC':
        #    pdb.set_trace()
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
            timedelta_str='RuntimeError accessing last time element '+str(err)
            return timedelta_str
            #pdb.set_trace()
        if ishours >= 0:
            last_time=offset+dt.timedelta(hours=int(asset_time[-1]))
        else:
            last_time=offset+dt.timedelta(seconds=int(asset_time[-1]))
        #pdb.set_trace()
        time_delta=now-last_time.replace(tzinfo=dt.timezone.utc)

        # offset date is either at -1 or -2 if it has hours:minutes:seconds
        # C-HARM is hours since X (time) no hours:mintues:seconds
        # UCSC ROMS is hours since Y (time) time has hours:minutes:seconds
        # NEMURO is hours since W (time) time has hours:minutes:seconds
        # COAMPS is seconds since Z (time) time has hours:minutes:seconds
        # WCOFS is seconds since U (ocean_time) time has no hours:minutes:seconds
        # SFBOFS is hours since V (ocean_time) time has hours:minutes:seconds
    if (iserddap > 0) or (isstation > 0):
        # is it sensor data or glider data
        # need to define the URL etc to read from
        # is it a glider or shore station? how can we tell?  assetID and assetURL don't really help
        # shore station
        caloos=assetURL.find('caloos')
        cencoos=assetURL.find('cencoos')
        sccoos=assetURL.find('sccoos')
        #pdb.set_trace()
        if (cencoos > 0) or (caloos > 0):
            try:
                asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
            except:
                asset_df=pd.read_csv('https://erddap.sensors.axds.co/erddap/tabledap/{}.csv?time'.format(assetID))
            # was this a HTTP error or the wrong URL?
        if sccoos > 0:
            # this is for the HABMAP stations different ERDDAP
            asset_df=pd.read_csv('https://erddap.sccoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
        #asset_df=pd.read_csv(f'https://erddap.cencoos.org/erddap/tabledap/{assetID}.csv?time')
        #asset_df=pd.read_csv(f'https://erddap.sensors.axds.co/erddap/tabledap/{erddapID}.csv?time')
        last_time = dt.datetime.strptime(asset_df['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
        time_delta = now - last_time
       
   # parse for more meaningful output
    #pdb.set_trace()
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

def create_clean_csv(outputfile):
    '''
    Create a CSV file with column headers
    '''
    with open(outputfile,'w',newline='') as csvfile:
        fieldnames=['Asset','timeDelta','caloosLink'] # for shore stations add 'gsheetsStatus'
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()

def write_to_csv(asset,timedelta_str,caloos_link,outputfile):
    '''
    Writes the timedelta string values for each asset as a new row in a CSV file.
    '''
    with open(outputfile,'a',newline='') as csvfile:
        fieldnames=['Asset','timeDelta','caloosLink'] # again shore station add 'gsheetsStatus'
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writerow({'Asset':asset,'timeDelta':timedelta_str,'caloosLink':caloos_link})



# main body of code
if __name__=="__main__":
    #fout=open('/home/flbahr/ingest_status_data.txt','w')
    msg=EmailMessage()
    msg['Subject']='Data ingest status'
    msg['From']='flbahr@mbari.org'
    msg['to']='flbahr@mbari.org'
    msgtxt=""

    outputfile='asset_timedelta.csv'
    create_clean_csv(outputfile=outputfile)
    [stationnames,stationID,stationURL,modelnames,modelID,modelURL,glidernames,gliderID,gliderURL,gliderioosURL,ifcbnames,ifcbID,ifcbURL,habnames,habID,habURL]=get_assets()
    for i in np.arange(0,len(stationnames)):
        print(stationID[i])
        timedelta_str=get_asset_delta(stationID[i],stationURL[i])
        write_to_csv(asset=stationnames[i],timedelta_str=timedelta_str,caloos_link=stationURL[i],outputfile=outputfile)
        msgtxt+=stationnames[i]+', '+timedelta_str+'\n'
    msgtxt+='\n'
    for i in np.arange(0,len(habnames)):
        print(habID[i])
        timedelta_str=get_asset_delta(habID[i],habURL[i])
        write_to_csv(asset=habnames[i],timedelta_str=timedelta_str,caloos_link=habURL[i],outputfile=outputfile)
        msgtxt+=habnames[i]+', '+timedelta_str+'\n'
    msgtxt+='\n'
    for i in np.arange(0,len(modelnames)):
        print(modelID[i])
        timedelta_str=get_asset_delta(modelID[i],modelURL[i])
        write_to_csv(asset=modelnames[i],timedelta_str=timedelta_str,caloos_link=modelURL[i],outputfile=outputfile)
        msgtxt+=modelnames[i]+', '+timedelta_str+'\n'
    msgtxt+='\n'
    for i in np.arange(0,len(glidernames)):
        print(gliderID[i])
        timedelta_str=get_asset_delta(gliderID[i],gliderURL[i])
        write_to_csv(asset=glidernames[i],timedelta_str=timedelta_str,caloos_link=gliderURL[i],outputfile=outputfile)
        msgtxt+=glidernames[i]+', '+timedelta_str+'\n'
    msgtxt+='\n'
    for i in np.arange(0,len(ifcbnames)):
        print(ifcbID[i])
        # can't just do the above since IFCB dashboard doesn't operate in the same way....
        now=dt.datetime.now()
        # lets not limit to yesterday and look 2 months back?
        yesterday=now+dt.timedelta(days=-60)
        #yesterday=now+dt.timedelta(days=-1)
        start=str(yesterday.year)+'-'+str(yesterday.month)+'-'+str(yesterday.day)
        stop=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        samples=get_bins_in_range(start,stop,ifcbID[i],'https://ifcb.caloos.org')
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
                #timedelta_str = f"{days} days, {hours} hours, {minutes} minutes"
            elif hours > 0:
                timedelta_str="{} hours, {} minutes".format(hours,minutes)
                #timedelta_str = f"{hours} hours, {minutes} minutes"
            elif minutes > 0:
                timedelta_str="{} minutes".format(minutes)
                #timedelta_str = f"{minutes} minutes"
            else:
                timedelta_str = "< 1 minute"        
        except:
            timedelta_str=samples
        write_to_csv(asset=ifcbnames[i],timedelta_str=timedelta_str,caloos_link=ifcbURL[i],outputfile=outputfile)
        try:
            msgtxt+=ifcbnames[i]+', '+timedelta_str+'\n'
        except:
            msgtxt+=ifcbnames[i]+', no data\n'
    now=dt.datetime.now(tz=dt.timezone.utc)
    print('Set message payload')
    msg.set_payload(msgtxt)
    print('Set localhost')
    s=smtplib.SMTP('localhost')
    print('Send message')
    s.send_message(msg)
    print ('quit mail')
    s.quit()
    # push file to webserver
    os.system('scp /home/flbahr/asset_timedelta.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
    
