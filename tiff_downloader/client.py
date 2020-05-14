import io
import os
import requests
from pathlib import Path
from pyDataverse.api import Api


class DataverseFileClient:
    CHUNK_SIZE = 2048

    def __init__(self, dataverse_api: Api, file_open=io.open):
        self.file_open = file_open
        self.url = dataverse_api.native_api_base_url
        self.api_token = dataverse_api.api_token

    def save_from(self, file_id, destination, file_version=1, params=None):
        query_str = f'/access/datafile/{file_id}'
        file_url = self.url + query_str

        stream = requests.get(file_url, params=params, stream=True)

        path = Path(os.path.dirname(destination)).mkdir(parents=True, exist_ok=True)
        with self.file_open(destination, 'wb') as file:
            for chunk in stream.iter_content(self.CHUNK_SIZE):
                file.write(chunk)

        return path

