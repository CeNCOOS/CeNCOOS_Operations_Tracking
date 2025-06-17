#!/bin/csh
#source /home/pdaniel/anaconda3/bin/ops_dashboard_v2/bin/activate

# shore stations
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/shorestations.py
scp /home/mlebrec/system_state/csv_output/stations_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60

# models
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/model_status.py
scp /home/mlebrec/system_state/csv_output/model_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60

# calhabmap
#cd /home/mlebrec/system_state
#/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/habmap_status.py
#scp /home/mlebrec/system_state/csv_output/model_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
# sleep 60

# ifcbs
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/ifcb_status.py
scp /home/mlebrec/system_state/csv_output/ifcb_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60

# gliders
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/glider_status.py
scp /home/mlebrec/system_state/csv_output/glider_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60

# ndbc 
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/ndbc_status.py
scp /home/mlebrec/system_state/csv_output/ndbc_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60

# cdip
cd /home/mlebrec/system_state
/home/pdaniel/anaconda3/envs/ops_dashboard_v2/bin/python3.10 /home/mlebrec/system_state/scripts/cdip_status.py
scp /home/mlebrec/system_state/csv_output/cdip_timedelta.csv mlebrec@Skyrocket8:/var/www/html/data/system_state/
sleep 60