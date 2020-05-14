import json
import os
import shutil
from pathlib import Path

import falcon
from pyvips import Image

from tiff_downloader import settings
from tiff_downloader.client import DataverseFileClient
from tiff_downloader.hooks import required_params


class Uploader:
    """
    Uploader transfers given TIFF files from Dataverse instance to designated directory. During this process
    file is being converted to Tiled Multi-Resolution (or Tiled Pyramidal) TIFF.
    """

    def __init__(self, dataverse_client):
        """
        Init function allowing for use of different dataverse client

        Parameters
        ----------
        dataverse_client: client object based on pyDataverse providing .get_dataset() method, native_api_base_url
        and api_token fields
        """
        self.dataverse_client = dataverse_client

    @falcon.before(required_params('file_id', 'dataset_pid'))
    def on_get(self, req, resp):
        """
        Method serving GET request.

        It downloads file form Dataverse server, saves it to temporary file then converts it to filed Multi-Resolution
        (or Tiled Pyramidal) TIFF and saves converted file to designated folder.

        """
        file_id = req.params['file_id']
        dataset_pid = req.params['dataset_pid']

        # get dataset form dataverse, if it doesn't exists forward error to client
        dv_dataset = self.dataverse_client.get_dataset(dataset_pid)
        if dv_dataset.status_code != 200:
            raise falcon.HTTPBadRequest('Dataverse returned an error', dv_dataset.text)
        # decode response to python dict
        dv_dataset_dict = json.loads(dv_dataset.content.decode("utf-8"))['data']

        # get metadata for requested file
        file_metadata = next(
            item for item in dv_dataset_dict['latestVersion']['files'] if str(item['dataFile']['id']) == file_id)
        filename = file_metadata['dataFile']['filename']
        # build filepath and replace / to - in dataset doi for better folders management
        filepath = os.path.join(dv_dataset_dict['storageIdentifier'][7:].replace('/', '-'), filename)
        tmp_filepath = os.path.join(settings.TEMP_DIR, filepath)
        tiff_server_filepath = os.path.join(settings.TIFF_SERVER_ROOT, filepath)

        # download file only if it doesn't exist yet
        if not os.path.exists(tmp_filepath):
            DataverseFileClient(self.dataverse_client).save_from(file_id=file_id, destination=tmp_filepath)

        # convert file only if it isn't converted yet
        if not os.path.exists(tiff_server_filepath):
            img = Image.new_from_file(tmp_filepath)

            Path(os.path.dirname(tiff_server_filepath)).mkdir(parents=True, exist_ok=True)
            img.tiffsave(tiff_server_filepath, compression='jpeg', pyramid=True, tile=True, tile_width=512,
                         tile_height=512)

            shutil.rmtree(os.path.dirname(tmp_filepath))

        # return relative path to converted file on TIFF server
        resp.body = json.dumps({'filepath': filepath})
