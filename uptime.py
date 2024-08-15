import numpy as np
import xarray as xr
import pandas as pd
import datetime as dt
from datetime import timedelta
import requests
import json
import sys
import matplotlib.pyplot as plt
import pdb
# code to compute uptime for assets
# the code assumes that the asset samples at regular intervals
# Do we need to deal with irregular interval sampling?
# do we need a units measure for this so we know what the sample interval is?
#
def uptime(seriestime,sampleinterval,starttime,endtime,gaptime):
    # sample interval is in minutes
    # gaptime is in hours
    # maybe we need to be consistent
    # also series time?
    # if seriestime is not in python datetime format do that
    try:
        seriestime=pd.to_datetime(seriestime)
    except:
        pass
    # compute first difference to see where the gaps are
    deltaseries=seriestime.diff()
    # flip the time series back to front (could not do this before diff
    # due to some weirdness in the computation
    seriestime=seriestime[::-1]
    # reset the index, but this keeps the old index as a column
    seriestime=seriestime.reset_index()
    # remove the old index column since we don't need it.
    seriestime=seriestime.drop('index',axis=1)
    # flip the differences also back to front so we can find out
    # from the present time when the first gap was backwards from there.
    deltaseries=deltaseries[::-1]
    # do the same as with time to get a new index
    deltaseries=deltaseries.reset_index()
    deltaseries=deltaseries.drop('index',axis=1)
    # since python does things in nanoseconds convert from them to a
    # more useful time interval
    pdb.set_trace()
    deltaseries=deltaseries/1e9
    deltaseries=deltaseries.astype(float)
    # convert to hours
    deltaseries=deltaseries/60.0/60.0
    # find where the first gap of a size is
    gindex=np.where(deltaseries > gaptime)
    gindex=gindex[0]
    # time since gap of size
    guptime=seriestime['time'][0]-seriestime['time'][gindex[0]]
    lindex=(seriestime['time'] >= starttime)&(seriestime['time'] <= endtime)
    subsettime=seriestime['time'][lindex]
    # get how many samples where taken during the specified time interval
    numsample=len(subsettime)
    # compute the total number of days during the specified interval
    totaldays=(endtime-starttime).days
    # using the number of samples estimate the number days that where sampled
    # This does not mean that the sampling was continuous
    actualdays=(numsample*sampleinterval)/60/24
    # compute the fractional time that was sampled
    percentdays=100*(actualdays/totaldays)
    # pass the values back ?
    return [guptime,totaldays,actualdays,percentdays]
    
