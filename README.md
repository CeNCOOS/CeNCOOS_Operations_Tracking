### This repository is used for keeping track of the operation of CeNCOOS infrastructure and data products 
The repository consists of various scripts for each CeNCOOS system that needs to be monitored. This operations tracking is ultimately published on this webpage: [https://www.cencoos.org/operations-dashboard/](https://www.cencoos.org/operations-dashboard/) 

**The types of datastreams that this code is currently checking regularly include:**
- CeNCOOS funded shore stations
- Regional model outputs
- High Frequency Radar products
- CalHABMAP sampling
- Imaging FlowCytobots (IFCBs)
- Gliders
- National Data Buoy Center (NDBC) Buoys
- Coastal Data Information Program (CDIP) Buoys
- Data products developed in-house
- Matlab scripts managed by Fred Bahr

**The directory structure is as follows:**
- `ag_grid` : JavaScript code to produce an interactive table for each datastream type using [AG Grid](https://www.ag-grid.com/), containing information about system status. This code is deployed on the CeNCOOS webserver.

- `csv_output` : csv files that are updated regularly (hourly) with information about system status, to be fed into the AG-Grid. These csv files are produced on the concave virtual machine managed by MBARI.

- `gsheet` : contains a JSON file and a Python script for accessing comments populated in a [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1-HcKNYpRJmm41R9zXwUGOvWBo917Kh_1t_FLRAH9UlQ/edit?gid=0#gid=0). Information from this spreadsheet is added as a column in several tables on the operations dashboard to provide more context as to why a system may be down.

- `json_files` : several JSON files used to access data fom each datatype, with dataset names and end-point information for fetching most recent data. 

- `scripts` : Python and bash scripts used for generating status csv files for different datastream types. 

- `testing` : various scripts and jupyter notebooks used for testing different stages in the pipeline.

![Workflow Diagram](https://github.com/CeNCOOS/CeNCOOS_Operations_Tracking/blob/main/operations-dashboard.drawio.png?raw=true)
