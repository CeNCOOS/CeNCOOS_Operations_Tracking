import numpy as np
import pandas as pd
# IFCB API functions
import requests
import json
import pandas as pd
import numpy as np
import pdb
def get_datasets(dashboard_url):
    """Return a list dashboard datasets from the API

    Args:
        dashboard_url (str): base url of an IFCB dashboard (V2)
    
    Returns:
        list: list of dataset names
    """
    request_rul = os.path.join(dashboard_url, 'api/filter_options')
    response=requests.get(request_rul)
    content=response.content
    content=json.loads(content)
    
    return content['dataset_options']
def get_bins_in_range(start_date, end_date, dataset_name, base_dashboard_url='https://ifcb.caloos.org'):
    """ Given a start date and end date, request all of the ifcb sampled from a given instrument feed

    Args:
        start_date (str): Start date string in the form of yyyy-mm-dd
        end_date (str): End date string in the form of yyyy-mm-dd
    Returns: 
        (pd.DataFrame): dataframe with a series of bin ids 
    """
    # Dates should be of the 
    url = f"{base_dashboard_url}/{dataset_name}/api/feed/temperature/start/{start_date}/end/{end_date}"
    response=requests.get(url)
    
    if response.status_code==200:
        content=response.content
        content=json.loads(content)
        content=pd.DataFrame.from_dict(content)
        try:
            content["pid"]=content["pid"].map(lambda x: x.lstrip(f"{base_dashboard_url}/{dataset_name}/"))
            content=content["pid"]
            return(content)
        except:
            if content.empty:
                an_empty_set=[]
            return(an_empty_set)
    else:
        print('Failed to get all bins with range with code: '+response.status_code)
        return(response.status_code)
