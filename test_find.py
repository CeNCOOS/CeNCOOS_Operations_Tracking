import json
hab_file='habmap_stations.json'
f=open(hab_file)
data=json.load(f)
habnames=[]
habID=[]
habURL=[]
for i in data:
    habnames.append(i['stationName'])
    habID.append(i['datasetID'])
    habURL.append(i['caloos_link'])
f.close()
