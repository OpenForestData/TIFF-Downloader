import io
import os
import requests
from pathlib import Path
from pyDataverse.api import Api


class DataverseFileClient:
    # Chunk size for TIFF streams
    CHUNK_SIZE = 2048

    def __init__(self, dataverse_api: Api, file_open=io.open):
        """
        Init allowing use of different dataverse API and different file open function for better testing.

        Parameters
        ----------
        dataverse_api: client object based on pyDataverse providing .get_dataset() method, native_api_base_url
        and api_token fields
        file_open: file open function
        """
        self.file_open = file_open
        self.url = dataverse_api.native_api_base_url
        self.api_token = dataverse_api.api_token

    def save_from(self, file_id, destination, params=None):
        """
        Function downloads given file and saves it to destination directory

        Parameters
        ----------
        file_id: dataverse id of datafile
        destination: path + filename where the file should be saved
        params: request params

        """
        query_str = f'/access/datafile/{file_id}'
        file_url = self.url + query_str

        # get response as stream
        stream = requests.get(file_url, params=params, stream=True)

        # creates destination path if it doesn't exists
        Path(os.path.dirname(destination)).mkdir(parents=True, exist_ok=True)
        # load file stream chunk by chunk
        with self.file_open(destination, 'wb') as file:
            for chunk in stream.iter_content(self.CHUNK_SIZE):
                file.write(chunk)

