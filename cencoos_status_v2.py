### Script for calculating the amount of time since the last update was recorded on ERDDAP for CeNCOOS coastal shore stations 
### and writing the output to a CSV file for further use ####################################################################
### Marine Lebrec - June 2024 ###############################################################################################


# Import libraries
import pandas as pd
import datetime as dt
import json
import csv

# Define functions
def get_all_stations():
    '''
    Fetch station names from the station_names.json file"
    '''
    station_file = 'station_names.json'
    f = open(station_file)
    data = json.load(f)
    stationnames = []
    for i in data:
        stationnames.append(i['stationName'])
    return stationnames 

def get_erddapid(station_file, station_name):
    '''
    Fetch ERDDAP IDs from the JSON file and station name
    '''
    f = open(station_file)
    data = json.load(f)

    for station in data:
            if station['stationName'] == station_name:
                return station['datasetID']
            
def get_timedelta(erddapID):
    '''
    Calculate the time delta between the present time and the latest time-point captured on ERDDAP.
    Note that both time points are in UTC.
    '''

    now = dt.datetime.now(tz=dt.timezone.utc)
    df = pd.read_csv(f'https://erddap.sensors.axds.co/erddap/tabledap/{erddapID}.csv?time')
    last_time = dt.datetime.strptime(df['time'].iloc[-1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
    time_delta = now - last_time

    # parse for more meaningful output
    days = time_delta.days
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        timedelta_str = f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        timedelta_str = f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        timedelta_str = f"{minutes} minutes"
    else:
        timedelta_str = "< 1 minute"
    
        return timedelta_str

def create_clean_csv(outputfile):
     '''
     Creates a clean CSV with proper column headers
     '''
     with open(outputfile, 'w', newline='') as csvfile:
            fieldnames = ['stationName', 'timeDelta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
     
     
def write_to_csv(station, timedelta_str, outputfile):
    '''
    Writes the timedelta string values for each station as a new row in a CSV file.
    '''
    with open(outputfile, 'a', newline='') as csvfile:
        fieldnames = ['stationName', 'timeDelta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'stationName': station, 'timeDelta': timedelta_str})

if __name__ == "__main__":
    outputfile = 'stations_timedelta.csv'
    create_clean_csv(outputfile = outputfile)

    for station in get_all_stations():
        erddapid = get_erddapid(station_file = 'station_names.json', station_name = station)
        timedelta_str = get_timedelta(erddapID=erddapid)
        write_to_csv(station = station, timedelta_str = timedelta_str, outputfile = outputfile)
    
    now = dt.datetime.now(tz=dt.timezone.utc)
    print(f'cencoos_status_v2.py ran successfully at {now} UTC')