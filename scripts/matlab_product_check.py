import os
import time
import numpy as np
import datetime as dt
import pdb
from ftplib import FTP
# setup access to MBARI FTP
ftp_host="ftp.mbari.org"
ftp_user="anonymous"
ftp_pw="flbahr@mbari.org"
# login and go to file directory
ftp=FTP(ftp_host)
ftp.login(user=ftp_user,passwd=ftp_pw)
ftp.cwd("pub/flbahr/error")
ftp.sendcmd('TYPE i')
# files to check on
filelist=['climate_run.err',
          'climate_run_Arena.err',
          'climate_woa.err',
          'copyerr.err',
          'getsea.err',
          'glider_a.err',
          'glider_c.err',
          'glider_woa.err',
          'oa_alarm.err',
          'pushit.err',
          'putsea.err',
          'puttext.err',
          'river.err',
          'wind_get.err']
lf=len(filelist)
nf=np.arange(0,lf)
ferr=np.array([])
mtime=np.array([])
# get the size in bytes of the files
for fil in nf:
    fsize=ftp.size(filelist[fil])
    ferr=np.append(ferr,fsize)
for fil in nf:
    mtmp=ftp.sendcmd('MDTM '+filelist[fil])
    mtmp=dt.datetime.strptime(mtmp[4:],'%Y%m%d%H%M%S')
    mtime=np.append(mtime,mtmp)
ftp.quit()
# text for output 
outputbase=['Trinidad glider climate run ',
            'Line 56 glider climate run ',
            'Glider using World Ocean Atlas ',
            'Copy files to webserver ',
            'Get seaglider files ',
            'Line56 glider climate run ',
            'Trinidad glider climate run ',
            'Climate run with World Ocean Atlas ',
            'OA watch circle alarm ',
            'Push Trinidad files to GliderDAC ',
            'Push Trinidad files to GliderDAC second test ',
            'Push data to Webserver ',
            'River Sonde data access ',
            'Get wind data ']
# write out the output
fout=open('csv_output/matlab_status_run.csv','w')
fout.write('Product description , number of bytes in error file, time file created\n')
for fil in nf:
    fout.write(outputbase[fil]+', '+str(ferr[fil])+', '+str(mtime[fil])+'\n')
# close and finish
fout.close()
