### Script for calculating the amount of time since the last update was recorded on ERDDAP for CeNCOOS coastal shore stations 
### and writing the output to a CSV file for further use ####################################################################
### Marine Lebrec - June 2024 ###############################################################################################


# Import libraries
import pandas as pd
import datetime as dt
import json
import csv
import gspread
from google.oauth2.service_account import Credentials

station_file = 'json_files/station_names.json'

# Define functions
def get_all_stations(station_file):
    '''
    Fetch station names from the station_names.json file"
    '''
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

def get_caloos_link(station_file, station_name):
    '''
    Fetch CalOOS links from the JSON file and station name
    '''
    f = open(station_file)
    data = json.load(f)
    for station in data:
            if station['stationName'] == station_name:
                return station['caloos_link']

def get_timedelta(erddapID):
    '''
    Calculate the time delta between the present time and the latest time-point captured on ERDDAP.
    Note that both time points are in UTC.
    '''

    now = dt.datetime.now(tz=dt.timezone.utc)
    try:

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
    
    except Exception as e:
        #print(e)
        timedelta_str = 'Unable to access data for this site via ERDDAP'
        
    return timedelta_str

def create_clean_csv(outputfile):
     '''
     Creates a clean CSV with proper column headers
     '''
     with open(outputfile, 'w', newline='') as csvfile:
            fieldnames = ['stationName', 'timeDelta', 'caloosLink', 'gsheetsStatus']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
     
     
def write_to_csv(station, timedelta_str, caloos_link, gsheets_status, outputfile):
    '''
    Writes the timedelta string values for each station as a new row in a CSV file.
    '''
    with open(outputfile, 'a', newline='') as csvfile:
        fieldnames = ['stationName', 'timeDelta', 'caloosLink', 'gsheetsStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'stationName': station, 'timeDelta': timedelta_str, 'caloosLink': caloos_link, 'gsheetsStatus': gsheets_status})


def get_gspread_status(station_file, station_name):
    ''' 
    Fetch the status of the station from the Google Sheet
    https://docs.google.com/spreadsheets/d/1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ/edit?gid=0#gid=0
    '''
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("gsheet/credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ"
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet("ShoreStations")

    # Load JSON station file
    with open(station_file) as f:
        data = json.load(f)

    # Get column A values (station names from the sheet)
    sheet_names = worksheet.col_values(1)

    for station in data:
        try:
            row_idx = sheet_names.index(station['stationName']) + 1
            if station['stationName'] == station_name:
                cell_value = worksheet.cell(row_idx, 2).value
                return cell_value
        except ValueError:
            # station['stationName'] not found in sheet_names
            pass

    # No match found
    return None

if __name__ == "__main__":
    station_file = 'json_files/station_names.json'
    outputfile = 'csv_output/stations_timedelta.csv'

    create_clean_csv(outputfile = outputfile)

    for station in get_all_stations(station_file=station_file):
        erddapid = get_erddapid(station_file = station_file, station_name = station)
        caloos_link = get_caloos_link(station_file = station_file, station_name = station)
        timedelta_str = get_timedelta(erddapID=erddapid)
        gsheets_status = get_gspread_status(station_file = station_file, station_name = station)
        write_to_csv(station = station, timedelta_str = timedelta_str, caloos_link = caloos_link, gsheets_status = gsheets_status, outputfile = outputfile)
    
    now = dt.datetime.now(tz=dt.timezone.utc)
    print(f'cencoos_status_v2.py ran successfully at {now} UTC')