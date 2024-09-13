import json
import netCDF4
import time
import pandas as pd

file='c:/Users/flbahr/station_up_time/model_names.json'
f=open(file)
data=json.load(f)
assetname=[]
assetid=[]
asseturl=[]
for i in data:
    assetname.append(i['modelName'])
    assetid.append(i['datasetID'])
    asseturl.append(i['caloos_link'])
f.close()
#url="http://thredds.cencoos.org/thredds/dodsC/CCSNRT_NEMURO.nc"
#asset_array=netCDF4.Dataset(url)
#asset_time=asset_array['time']
#units=asset_time.units
#subunits=units.split()
erddapID="OSU686-20240412T0000"
string='https://erddap.cencoos.org/erddap/tabledap/'+erddapID+'.csv?time'
print(string)
#test_df=pd.read_csv(string)
#asset_df=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/'+erddapID+'.csv?time')
asset_df=pd.read_csv(f'https://erddap.sensors.axds.co/erddap/tabledap/{erddapID}.csv?time')
#string='https://erddap.cencoos.org/erddap/tabledap/OSU686-20240412T0000.csv?time'
#df=pd.read_csv(string)
