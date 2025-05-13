#
#
#
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
#import smtplib
#from email.message import EmailMessage
#from ifcb_helper import get_bins_in_range, get_datasets
#from sfbofs_api_times import sfbofs_api_times
import os
#
# get assets from json files
#
def get_assets(aname):
    '''
    Fetch asset names based upon type and asset name json file

    aname is the json file containging the asset information

    '''
    f=open(aname)
    data=json.load(f)
    # check size of first element that will determine how many objects are returned
    nvalues=len(data[0])
    keyvalue=list(data[0].keys())
    assetnames=[]
    assetID=[]
    assetURL=[]
    if nvalues > 3:
        assetIOOSURL=[]
    for i in data:
        assetnames.append(i[keyvalue[0]])
        assetID.append(i[keyvalue[1]])
        assetURL.append(i[keyvalue[2]])
        if nvalues > 3:
            assetIOOSURL.append(i[keyvalue[3]])
    f.close()
    if nvalues > 3:
        return [assetnames, assetID, assetURL,assetIOOSURL]
    else:
        return [assetnames, assetID, assetURL]
#
# 
#


    
def create_clean_csv(outputfile,asset_type,gsheet):
    '''
    Create a CSV file with column headers
    create_clean_csv(outputfile,asset_type,gsheet)
    where:
    outputfile is the name for the output file
    asset_type is a string for the first column header (i.e. shorestation, glider, model, etc)
    gsheet is whether there is a google sheet associated with the data (True or False)

    Example:
    create_clean_csv('shorestations_status.csv','stationName','True')
    
    '''
    with open(outputfile,'w',newline='') as csvfile:
        if gsheet==True:
            fieldnames=[asset_type,'timeDelta','caloosLink','gsheetsStatus'] # for shore stations add 'gsheetsStatus'
        else:
            fieldnames=[asset_type,'timeDelta','caloosLink']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()

def write_to_csv(asset_type,asset,timedelta_str,caloos_link,outputfile,*gsheet):
    '''
    Writes the timedelta string values for each asset as a new row in a CSV file.
    write_to_csv(asset_type,asset,timedelta_str,caloos_link,outputfile,*gsheet)
    Where:
    asset_type is type of asset
    asset is  the name of the asset
    timedelta_str is the time difference
    caloos_link is the link to the data at Axiom
    outputfile is the file name to write to
    *gsheet is optional argument with google sheet data
    Example:

    *arg for optional argument? **kwargs is for dictionary set of arguments
    
    '''
    with open(outputfile,'a',newline='') as csvfile:
        if not gsheet:
            fieldnames=['Asset','timeDelta','caloosLink'] # again shore station add 'gsheetsStatus'
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writerow({'Asset':asset,'timeDelta':timedelta_str,'caloosLink':caloos_link})
        else:
            fieldnames=['Asset','timeDelta','caloosLink','gsheetsStatus'] # again shore station add 'gsheetsStatus'
            writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writerow({'Asset':asset,'timeDelta':timedelta_str,'caloosLink':caloos_link,'gsheetsStatus':gsheet})

                               
        
