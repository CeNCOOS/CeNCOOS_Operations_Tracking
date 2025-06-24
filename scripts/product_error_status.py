#
# This code is used to check if a product ran error free.
# The code prints the size of the error file in bytes to a file
# (a mail message will be sent to flbahr for a while to check that all output is working
# this will be stopped when it is confirmed that the code outputs properly)
# 
import os
import time
import numpy as np
from sfbofs_api_times import sfbofs_api_times
import pdb
# code needed for e-mail support
#import smtplib
#from email.message import EmailMessage
# Code to set up e-mail message
#msg=EmailMessage()
#msg['Subject']='Product error file output'
#msg['From']='flbahr@mbari.org'
#msg['To']='flbahr@mbari.org'
# output file for error status values
fout=open('/home/flbahr/product_error_status.csv','w')
# first data path to check and the list of files to check
basedir='/home/flbahr/'
filelist=['ga4daily.err',
          'update.err',
          'getwcofs3.err',
          'lastmonth.err',
          'heatwave.err',
          'truncate.err',
          'mergeerr.err',
          'ploterr.err',
          'filepusherr.err']
outputbase=['Google analytics: daily user access count append to data file',
            'Google analytics: monthly user access count append to data file',
            'Heat Wave: get current days WCOFS SST from Amazon S3',
            'Heat Wave: get last months WCOFS SST from Amazon S3',
            'Heat Wave: Run the actual heatwave code',
            'Heat Wave: Reformat of WCOFS SST data',
            'Heat Wave: Merge the WCOFS SST data',
            'Heat Wave: Plot the output of the HeatWave code',
            'Transfer files (plots and other data) to webserver']
producturl=['https://cencoos.org/analytics-daily/',
            'https://cencoos.org/analytics-monthly/',
            '',
            '',
            'https://cencoos.org/marine-heatwave/',
            '',
            '',
            'https://cencoos.org/marine-heatwave/',
            '']
productnote=['Google analytics',
             'Google analytics',
             'internal Heatwave WCOFS daily SST data read',
             'internal Heatwave WCOFS last month SST data read',
             'Heatwave run',
             'Reformat WCOFS SST data for use with heatwave',
             'Merge WCOFS SST data for use with heatwave',
             'Plot output from Heatwave code',
             'Push files to webserver']
            
nf=np.arange(0,len(filelist))
msgtxt=""
fout.write('productDescription, errorFileInBytes, timeErrorFileCreated, productURL, comment\n')
for i in nf:
    try:
        file_size=os.path.getsize(basedir+filelist[i])
        ti_m=os.path.getmtime(basedir+filelist[i])
        modified_time=time.ctime(ti_m)
#        msgtxt+=filelist[i]+'\t'+str(file_size)+'\t'+modified_time+'\n'
#        print(filelist[i]+'\t'+str(file_size)+'\t'+modified_time)
        fout.write(outputbase[i]+', '+str(file_size)+', '+modified_time+','+producturl[i]+','+productnote[i]+'\n')
    except:
#        msgtxt+=filelist[i]+'\t\tfile not found\n'
#        print(filelist[i]+'\t\tfile not found')
        fout.write(outputbase[i]+', No data, File not found,'+producturl[i]+','+productnote[i]+'\n')
# Next directory to check product status   
basedir2='/home/pdaniel/'
filelist2=['upwell.err',
           'wavestat.err']
outputbase2=['CUTI and BEUTI update plots',
             'Wave statistics update ']
producturl2=['https://cencoos.org/cuti-and-beuti-upwelling-indices-post/',
             'https://cencoos.org/information-solutions/recent-waves/']
productnote2=['CUTI and BEUTI plots',
              'Wave Statistices plots']
nf2=np.arange(0,len(filelist2))
for i in nf2:
    try:
        file_size=os.path.getsize(basedir2+filelist2[i])
        ti_m=os.path.getmtime(basedir2+filelist2[i])
        modified_time=time.ctime(ti_m)
#        msgtxt+=filelist2[i]+'\t'+str(file_size)+'\t'+modified_time+'\n'
#        print(filelist2[i]+'\t'+str(file_size)+'\t'+modified_time)
        fout.write(outputbase2[i]+', '+str(file_size)+', '+modified_time+','+producturl2[i]+','+productnote2[i]+'\n')
    except:
#        msgtxt+=filelist2[i]+'\t\tfile not found\n'
#        print(filelist2[i]+'\t\tfile not found')
        fout.write(outputbase2[i]+', No data, File not found,'+producturl2[i]+','+productnote2[i]+'\n')

basedir3='/home/mlebrec/cron_logs/'
filelist3=['mbari_underway.err',
           'update_aggrid.err',
           'thoon_webserver.err',
           'thoon_processing.err']
outputbase3=['MBARI Underway pCO2 data processing',
            'System status status',
            'THOON data to webserver',
            'THOON data processing']
producturl3=['https://cencoos.org/data/underway/latest_file.csv',
             'https://cencoos.org/shore-station-operations-status/',
             'https://cencoos.org/thoon/',
             'https://cencoos.org/thoon/']
productnote3=['process latest underway pCO2 data',
              'create system status status',
              'THOON data to the webserver',
              'THOON data processing for plots']
nf3=np.arange(0,len(filelist3))
for i in nf3:
    try:
        file_size=os.path.getsize(basedir3+filelist3[i])
        ti_m=os.path.getmtime(basedir3+filelist3[i])
        modified_time=time.ctime(ti_m)
#        msgtxt+=filelist3[i]+'\t'+str(file_size)+'\t'+modified_time+'\n'
#        print(filelist3[i]+'\t'+str(file_size)+'\t'+modified_time)
        fout.write(outputbase3[i]+', '+str(file_size)+', '+modified_time+','+producturl3[i]+','+productnote3[i]+'\n')
    except Exception as e:
        pdb.set_trace()
#        msgtxt+=filelist3[i]+'\t\tfile not found\n'
#        print(filelist3[i]+'\t\tfile not found')
        fout.write(outputbase3[i]+', No data, File not found,'+producturl3[i]+','+productnote3[i]+'\n')

#apistr=sfbofs_api_times()
#fout.write(apistr)
fout.close()
#msgtxt+='\n'+apistr
#msg.set_payload(msgtxt)
#s=smtplib.SMTP('localhost')
#s.send_message(msg)
#s.quit()

# push file to webserver data directory
os.system('scp /home/flbahr/product_error_status.csv flbahr@skyrocket8.mbari.org:/var/www/html/data/system_state/')
