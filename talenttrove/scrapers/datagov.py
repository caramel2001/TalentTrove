import requests
from tqdm import tqdm
import pandas as pd
import numpy as np 

class DataGovCollection():

    def __init__(self, collection_id,verbose=True, *args, **kwargs):
        self.url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
        self.verbose=True
    
    def collect(self):
        response  = requests.get(self.url)
        
        datasets = response.json()['data']['collectionMetadata']['childDatasets']
        if self.verbose:
            print(f"Extracting {len(datasets)} datsets")
        datas=[]
        for dataset in tqdm(datasets):
            response  = requests.post(f"https://kjo15bc7zd.execute-api.ap-southeast-1.amazonaws.com/api/public/resources/{dataset}/generate-download-link")
            data = pd.read_csv(response.json()['url'])
            datas.append(data)
        return pd.concat(datas,axis=0)
    
    @staticmethod
    def filter(df):
        filter_data = df[df['entity_status_description'].str.contains('live',case=False)].copy()
        filter_data.replace('na',np.nan,inplace=True)
        return filter_data[['uen', 'entity_name', 'entity_type_description', 'company_type_description', 'entity_status_description','primary_ssic_code', 'primary_ssic_description',
       'primary_user_described_activity']]