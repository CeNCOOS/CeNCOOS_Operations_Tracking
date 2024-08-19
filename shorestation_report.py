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
from uptime import uptime
from dateutil.relativedelta import relativedelta
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
# get the current date and time
thenow=dt.datetime.now()
theyear=thenow.year
themonth=thenow.month
theday=thenow.day
# figure out what the start of the quarter is relative to present time
#
if themonth < 4:
    quarter_start=1
elif themonth >=4 and themonth < 7:
    quarter_start=4
elif themonth >=7 and themonth < 10:
    quarter_start=7
elif themonth >=10:
    quarter_start=10
# 
thequarter_start=dt.datetime(theyear,quarter_start,1,0,0,0,tzinfo=timezone.utc)
thequarter_end=dt.datetime(theyear,quarter_start+3,1,0,0,0,tzinfo=timezone.utc)
# we also want 6 months past
halfyear_start=dt.datetime(theyear,themonth,theday,0,0,0,tzinfo=timezone.utc)-relativedelta(months=6)
if themonth < 7:
    yeartouse=theyear-1
else:
    yeartouse=theyear
ioosyear_start=dt.datetime(yeartouse,7,1,0,0,0,tzinfo=timezone.utc)
#
# step 3) Get the time interval for the station
#
interval=[]
# mlml
interval.append(5)
# Hog Island
interval.append(5)
# Romberg EOS
interval.append(15)
# Santa Cruz Wharf
interval.append(5)
# Trinidad
interval.append(15)
# Bodega Seawater Intake
interval.append(4)
# Carquinez (not exactly 15 minutes for some reason)
interval.append(15)
# Fort Point (offline for now)
interval.append(6)
# Humboldt Bay
interval.append(15)
# Monterey Wharf
interval.append(20)
# Morro Bay
interval.append(10)
# Morro Bay BS1
interval.append(15)
# San Luis Bay CPXC1 has 1 minute but multiple values?
interval.append(1)
# Tuluwat
interval.append(15)

ls=1
time_since_last_gap=[]
quarter_days_up=[]
quarter_percent_uptime=[]
six_month_uptime=[]
six_month_percent_uptime=[]
ioos_year_uptime=[]
ioos_year_percent_uptime=[]
for istation in np.arange(0,ls):
    assetID=stationID[istation]
    print(assetID)
    asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/{}.csv?time'.format(assetID))
    seriestime=asset_df['time'][1:]
    gaptime=4
    [guptime,totaldays,actualdays,percentdays]=uptime(seriestime,interval[istation],thequarter_start,thequarter_end,gaptime)]
    [sixuptime,sixtotal,sixactual,sixpercent]=uptime(seriestime,interval[istation],halfyear_start,thenow,gaptime)
    [yruptime,yrtotal,yractual,yrpercent]=uptime(seriestime,interval[istation],ioosyear_start,thenow,gaptime)
    # how do we output the results?
    time_since_last_gap.append(guptime)
    quarter_days_up.append(actualdays)
    quarter_percent_uptime.append(percentdays)
    six_month_uptime.append(sixactual)
    six_month_percent_uptime.append(sixpercent)
    ioos_year_uptime.append(yractual)
    ioos_year_percent_uptime.append(yrpercent)


