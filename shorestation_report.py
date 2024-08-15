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
from ifcb_helper import get_bins_in_range, get_datasets
#
# As a first cut this will be an attempt to get the up time values for a shore station.
# We will want to change the name as we extend to other files.
# One hope is that we can get the glider stats from this file by keeping track of deployments in a json or csv file
#
#
# step 1) load the shore station json information
#''' 
#Fetch asset names from the appropriate json file
#'''
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
# step 2)
# get the current date and time and figure out
#
# step 3) Get the time vector for the shore station
#
#ls=len(stationID)
ls=1
for istation in np.arange(0,ls):
    assetID=stationID[istation]
    asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
#pdb.set_trace()