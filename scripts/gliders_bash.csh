#!/bin/csh
#source /home/pdaniel/anaconda3/bin/ops_dashboard_v2/bin/activate

# gliders
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/glider_status.py
scp /home/mlebrec/system_state/csv_output/glider_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
