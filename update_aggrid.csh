#!/bin/csh
source /home/pdaniel/anaconda3/bin/ops_dashboard/bin/activate
cd /home/mlebrec/station_up_time
/home/pdaniel/anaconda3/underway/bin/python /home/mlebrec/station_up_time/cencoos_status_v2.py
scp /home/mlebrec/station_up_time/stations_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/ops_aggrid/