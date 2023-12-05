import requests
from tqdm import tqdm
import pandas as pd
import numpy as np

import requests
import pandas as pd
import numpy as np
from tqdm import tqdm


class DataGovCollection:
    """
    A class for collecting and filtering data from the Data.gov API.

    Attributes:
        collection_id (str): The ID of the collection to retrieve data from.
        verbose (bool): Whether to display progress information during data collection.

    Methods:
        collect(): Collects data from the Data.gov API and returns a concatenated DataFrame.
        filter(df): Filters the provided DataFrame based on entity status description.

    """

    def __init__(self, collection_id, verbose=True, *args, **kwargs):
        """
        Initializes a DataGovCollection object.

        Args:
            collection_id (str): The ID of the collection to retrieve data from.
            verbose (bool, optional): Whether to display progress information during data collection.
                Defaults to True.

        """
        self.url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
        self.verbose = verbose

    def collect(self):
        """
        Collects data from the Data.gov API and returns a concatenated DataFrame.

        Returns:
            pd.DataFrame: The concatenated DataFrame containing the collected data.

        """
        response = requests.get(self.url)

        datasets = response.json()["data"]["collectionMetadata"]["childDatasets"]
        if self.verbose:
            print(f"Extracting {len(datasets)} datasets")
        datas = []
        for dataset in tqdm(datasets):
            response = requests.post(
                f"https://kjo15bc7zd.execute-api.ap-southeast-1.amazonaws.com/api/public/resources/{dataset}/generate-download-link"
            )
            data = pd.read_csv(response.json()["url"])
            datas.append(data)
        return pd.concat(datas, axis=0)

    @staticmethod
    def filter(df):
        """
        Filters the provided DataFrame based on entity status description.

        Args:
            df (pd.DataFrame): The DataFrame to be filtered.

        Returns:
            pd.DataFrame: The filtered DataFrame.

        """
        filter_data = df[
            df["entity_status_description"].str.contains("live", case=False)
        ].copy()
        filter_data.replace("na", np.nan, inplace=True)
        return filter_data[
            [
                "uen",
                "entity_name",
                "entity_type_description",
                "company_type_description",
                "entity_status_description",
                "primary_ssic_code",
                "primary_ssic_description",
                "primary_user_described_activity",
            ]
        ]


class DataGovCollection:
    def __init__(self, collection_id, verbose=True, *args, **kwargs):
        self.url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
        self.verbose = verbose

    def collect(self):
        response = requests.get(self.url)

        datasets = response.json()["data"]["collectionMetadata"]["childDatasets"]
        if self.verbose:
            print(f"Extracting {len(datasets)} datsets")
        datas = []
        for dataset in tqdm(datasets):
            response = requests.post(
                f"https://kjo15bc7zd.execute-api.ap-southeast-1.amazonaws.com/api/public/resources/{dataset}/generate-download-link"
            )
            data = pd.read_csv(response.json()["url"])
            datas.append(data)
        return pd.concat(datas, axis=0)

    @staticmethod
    def filter(df):
        filter_data = df[
            df["entity_status_description"].str.contains("live", case=False)
        ].copy()
        filter_data.replace("na", np.nan, inplace=True)
        return filter_data[
            [
                "uen",
                "entity_name",
                "entity_type_description",
                "company_type_description",
                "entity_status_description",
                "primary_ssic_code",
                "primary_ssic_description",
                "primary_user_described_activity",
            ]
        ]
