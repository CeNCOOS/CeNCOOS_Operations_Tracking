### This repository is used for keeping track of the operation of CeNCOOS infrastructure and data products 
The repository consists of various scripts for each CeNCOOS system that needs to be monitored.  Some systems will need to be updated as endpoints change. 
In particular, each glider swap requires and update of the glider_names.json file.  When the HF Radar endpoint changes those URLS will have to be updated also.

**The types of datastreams that this code is currently checking regularly include:**
- CeNCOOS funded shore stations
- Data products developed in-house

**The directory structure is as follows:**
- `ag_grid` : JavaScript code to produce an interactive table for each datastream type using [AG Grid](https://www.ag-grid.com/), containing information about system status. This code is deployed on the CeNCOOS webserver.

- `csv_output` : csv files that are updated regularly (hourly) with information about system status, to be fed into the AG-Grid. These csv files are produced on the concave virtual machine managed by MBARI.

- `gsheet` : contains a JSON file and a Python script for accessing real-time information about shore station status from technicians' comments populated in a [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ/edit?gid=0#gid=0). Information from this spreadsheet is added as a column in the shore station AG Grid table.

- `json_files` : several JSON files used to access data fom each datatype (e.g., shore stations, models, gliders).

- `scripts` : Python and bash scripts used for generating status csv files for different datastream types. 

- `testing` : various scripts and jupyter notebooks used for testing different stages in the pipeline.

![Workflow Diagram](https://github.com/CeNCOOS/CeNCOOS_Operations_Tracking/blob/main/operations-dashboard.drawio.png?raw=true)
