#!/bin/csh
#source /home/pdaniel/anaconda3/bin/ops_dashboard_v2/bin/activate
cd /home/mlebrec/station_up_time
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/station_up_time/scripts/shorestations.py
scp /home/mlebrec/station_up_time/csv_output/stations_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/ops_aggrid/