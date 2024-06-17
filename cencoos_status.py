# Code to check the status of CeNCOOS funded project ingest in the portal.
# Also to be use to monitor for problems/staleness.
#
# load some modules for use to read remote data and access time
#
import numpy as np
import xarray as xr
import pandas as pd
import datetime as dt
from datetime import timedelta
import requests
import json
import sys
import smtplib
from email.message import EmailMessage

import pdb
# This is a local module that will need to be put on the machine...
sys.path.insert(0,'/home/flbahr/')
import ifcb_api_access

#
msg=EmailMessage()
msg['Subject']='Data ingest status'
msg['From']='flbahr@mbari.org'
msg['To']='flbahr@mbari.org'
#
#

# Step 1 get the current time
now=dt.datetime.utcnow()
#
# read shore station data
#
mlml=pd.read_csv('https://erddap.sensors.axds.co/erddap/tabledap/mlml_mlml_sea.csv?time')
eos=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/tiburon-water-tibc1.csv?time')
scwharf=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/edu_ucsc_scwharf1.csv?time')
trin=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/edu_humboldt_tdp.csv?time')
bodega=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/bodega-bay-bml_wts.csv?time')
carquinez=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/carquinez.csv?time')
fortpoint=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/fort-point.csv?time')
humboldt=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/edu_humboldt_humboldt.csv?time')
monterey=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/mlml_monterey.csv?time')
morro=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/edu_calpoly_marine_morro.csv?time')
tuluwat=pd.read_csv('https://erddap.cencoos.org/erddap/tabledap/wiyot_tribe_indianisland.csv?time')
#
# Look at the last time of the data
#
tmlml=dt.datetime.strptime(mlml['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
teos=dt.datetime.strptime(eos['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tscwharf=dt.datetime.strptime(scwharf['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
ttrin=dt.datetime.strptime(trin['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tbodega=dt.datetime.strptime(bodega['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tcarquinez=dt.datetime.strptime(carquinez['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tfortpoint=dt.datetime.strptime(fortpoint['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
thumboldt=dt.datetime.strptime(humboldt['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tmonterey=dt.datetime.strptime(monterey['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
tmorro=dt.datetime.strptime(morro['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
ttuluwat=dt.datetime.strptime(tuluwat['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
#
# compute the time delta between the last time and "now"
#
dtrin=now-ttrin
dhumboldt=now-thumboldt
dtuluwat=now-ttuluwat
dbodega=now-tbodega
deos=now-teos
dfortpoint=now-tfortpoint
dcarquinez=now-tcarquinez
dscwharf=now-tscwharf
dmonterey=now-tmonterey
dmlml=now-tmlml
dmorro=now-tmorro
#
# At some point we need to output this information
#
# Temporarily print it out
#
msgtxt=""
msgtxt+='Trinidad is '+str(dtrin.days)+' Days and '+str(round(dtrin.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Humboldt is '+str(dhumboldt.days)+' Days and '+str(round(dhumboldt.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Tuluwat is '+str(dtuluwat.days)+' Days and '+str(round(dtuluwat.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Bodega is '+str(dbodega.days)+' Days and '+str(round(dbodega.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Fort Point is '+str(dfortpoint.days)+' Days and '+str(round(dfortpoint.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Carquinez is '+str(dcarquinez.days)+' Days and '+str(round(dcarquinez.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='EOS is '+str(deos.days)+' Days and '+str(round(deos.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Santa Cruz Wharf is '+str(dscwharf.days)+' Days and '+str(round(dscwharf.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Moss Landing is '+str(dmlml.days)+' Days and '+str(round(dmlml.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Monterey is '+str(dmonterey.days)+' Days and '+str(round(dmonterey.seconds/60/60,2))+' hours ahead/behind\n'
msgtxt+='Morro Bay is '+str(dmorro.days)+' Days and '+str(round(dmorro.seconds/60/60,2))+' hours ahead/behind\n'

print('Trinidad is '+str(dtrin.days)+' Days and '+str(round(dtrin.seconds/60/60,2))+' hours ahead/behind')
print('Humboldt is '+str(dhumboldt.days)+' Days and '+str(round(dhumboldt.seconds/60/60,2))+' hours ahead/behind')
print('Tuluwat is '+str(dtuluwat.days)+' Days and '+str(round(dtuluwat.seconds/60/60,2))+' hours ahead/behind')
print('Bodega is '+str(dbodega.days)+' Days and '+str(round(dbodega.seconds/60/60,2))+' hours ahead/behind')
print('Fort Point is '+str(dfortpoint.days)+' Days and '+str(round(dfortpoint.seconds/60/60,2))+' hours ahead/behind')
print('Carquinez is '+str(dcarquinez.days)+' Days and '+str(round(dcarquinez.seconds/60/60,2))+' hours ahead/behind')
print('EOS is '+str(deos.days)+' Days and '+str(round(deos.seconds/60/60,2))+' hours ahead/behind')
print('Santa Cruz Wharf is '+str(dscwharf.days)+' Days and '+str(round(dscwharf.seconds/60/60,2))+' hours ahead/behind')
print('Moss Landing is '+str(dmlml.days)+' Days and '+str(round(dmlml.seconds/60/60,2))+' hours ahead/behind')
print('Monterey is '+str(dmonterey.days)+' Days and '+str(round(dmonterey.seconds/60/60,2))+' hours ahead/behind')
print('Morro Bay is '+str(dmorro.days)+' Days and '+str(round(dmorro.seconds/60/60,2))+' hours ahead/behind')
#
# Get the available IFCBs
#
def get_bins_in_range(start_date, end_date, dataset_name, base_dashboard_url='https://ifcb.caloos.org'):
    """ Given a start date and end date, request all of the ifcb sampled from a given instrument feed

    Args:
        start_date (str): Start date string in the form of yyyy-mm-dd
        end_date (str): End date string in the form of yyyy-mm-dd
    Returns: 
        (pd.DataFrame): dataframe with a series of bin ids 
    """
    # Dates should be of the 
    url = f"{base_dashboard_url}/{dataset_name}/api/feed/temperature/start/{start_date}/end/{end_date}"
    response=requests.get(url)
    #print(url)
    #print(response.status_code)
    #print(dataset_name)
    # Response status can be 200 and still be an empty set
    if response.status_code==200:
        content=response.content
        content=json.loads(content)
        content=pd.DataFrame.from_dict(content)
        if content.empty:
            return(404)
        else:
            content["pid"]=content["pid"].map(lambda x: x.lstrip(f"{base_dashboard_url}/{dataset_name}/"))
            content=content["pid"]
            return(content)
    else:
        print('Failed to get all bins with range with code: '+response.status_code)
        return(response.status_code)




urlapi='https://ifcb.caloos.org/api/'
furl=urlapi+'filter_options'
response1=requests.get(furl)
content=response1.content
content=json.loads(content)
options=pd.DataFrame([content])
ifcbs=options['dataset_options'][0]
#print(ifcbs)
#
# looking for bodega-marine-lab, cal-poly-humboldt-hioc, mbari-power-buoy, santa-cruze-municipal-wharf, san-francisco-pier-17
#
sites=['bodega-marine-lab','cal-poly-humboldt-hioc','mbari-power-buoy','santa-cruz-municipal-wharf','san-francisco-pier-17']
lsites=len(sites)
lastday=now+dt.timedelta(days=-1)
start=str(lastday.year)+'-'+str(lastday.month)+'-'+str(lastday.day)
stop=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
for i in np.arange(0,lsites):
     theindex=ifcbs.index(sites[i])
     samples=get_bins_in_range(start,stop,ifcbs[theindex]) # why is this returning 200 and not 404 as below?
     try:
         if samples==404:
             msgtxt+='IFCB '+ifcbs[theindex]+' had no data\n'
             print('IFCB '+ifcbs[theindex]+' had no data')
         else:
             numdate=len(samples)
             msgtxt+='IFCB '+ifcbs[theindex]+' had '+str(numdate)+' samples\n'
             print('IFCB '+ifcbs[theindex]+' had '+str(numdate)+' samples')
     except:
        numdate=len(samples)
        msgtxt+='IFCB '+ifcbs[theindex]+' had '+str(numdate)+' samples\n'
        print('IFCB '+ifcbs[theindex]+' had '+str(numdate)+' samples')
#
# Glider days
#
# Is there a way to automate this?
#
urltrin='https://gliders.ioos.us/erddap/tabledap/OSU686-20240412T0000.csv?time'
trin=pd.read_csv(urltrin)
url67='https://gliders.ioos.us/erddap/tabledap/sp025-20240515T2040.csv?time'
line67=pd.read_csv(url67)
url57='https://gliders.ioos.us/erddap/tabledap/sp028-20240403T1628.csv?time'
line57=pd.read_csv(url57)
day1trin=dt.datetime.strptime(trin['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
day2trin=dt.datetime.strptime(trin['time'].iloc[1],'%Y-%m-%dT%H:%M:%SZ')
dtrin=day1trin-day2trin
day1_67=dt.datetime.strptime(line67['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
day2_67=dt.datetime.strptime(line67['time'].iloc[1],'%Y-%m-%dT%H:%M:%SZ')
d67=day1_67-day2_67
day1_57=dt.datetime.strptime(line57['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ')
day2_57=dt.datetime.strptime(line57['time'].iloc[1],'%Y-%m-%dT%H:%M:%SZ')
d57=day1_57-day2_57

msgtxt+=str(dtrin.days)+' Trinidad glider days\n'
msgtxt+=str(d57.days)+' Arena glider days\n'
msgtxt+=str(d67.days)+' Monterey glider days\n'
print(str(dtrin.days)+' Trinidad glider days')
print(str(d57.days)+' Arena glider days')
print(str(d67.days)+' Monterey glider days')
#
# Model times
#
# Model status
urlNEMURO='http://thredds.cencoos.org/thredds/dodsC/CCSNRT_NEMURO.nc'
# time is called time in this instance
urlUCSCROMS='http://thredds.cencoos.org/thredds/dodsC/UCSC.nc'
#urlCHARM='http://thredds.cencoos.org/thredds/dodsC/CHARM_NOWCAST_V2.nc'
#urlCHARMF='http://thredds.cencoos.org/thredds/dodsC/CHARM_FORECAST_V2.nc'
urlCOAMPS='http://thredds.cencoos.org/thredds/dodsC/COAMPS.nc'
urlCHARM ='http://thredds.cencoos.org/thredds/dodsC/CHARM_FORECAST_V3.nc'
#urlCHARM='https://coastwatch.pfeg.noaa.gov/erddap/griddap/wvcharmV3_0day.csv?time'
ctime=xr.open_dataset(urlCHARM)
ca=ctime['time'][-1].values

#pdb.set_trace()
#ctime=pd.read_csv(urlCHARM)
#nemuro=xr.open_dataset(urlNEMURO)
#ucscroms=xr.open_dataset(urlUCSCROMS)
coamps=xr.open_dataset(urlCOAMPS)
#
#cc=ctime['time'].iloc[-1]
ct=coamps['time'][-1]

import netCDF4
nc=netCDF4.Dataset(urlNEMURO)
time=nc.variables['time']
uc=netCDF4.Dataset(urlUCSCROMS)
utime=nc.variables['time']
nemurostart=dt.datetime(2013,1,1)
ucscstart=dt.datetime(2011,1,2)
nemurotime=nemurostart+timedelta(hours=time[-1].__int__())
ucsctime=ucscstart+timedelta(hours=utime[-1].__int__())
msgtxt+='Last ingest output of UCSC ROMS was '+str(ucsctime)+'\n'
msgtxt+='Last ingest output of UCSC NEMURO was '+str(nemurotime)+'\n'
msgtxt+='Last output of COAMPS was '+str(ct.values)+'\n'
msgtxt+='Last output of C-HARM was '+str(ca)+'\n'

print('Last ingest output of UCSC ROMS was '+str(ucsctime))
print('Last ingest output of UCSC NEMURO was '+str(nemurotime))
print('Last output of COAMPS was '+str(ct.values))
print('Last output of C-HARM was '+str(ca))

msg.set_payload(msgtxt)
s=smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
