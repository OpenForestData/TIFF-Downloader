import json
import os

import falcon

from tiff_downloader import settings
from tiff_downloader.client import DataverseFileClient
from tiff_downloader.hooks import required_params


class Uploader(object):

    def __init__(self, dataverse_client):
        self.dataverse_client = dataverse_client

    @falcon.before(required_params('file_id', 'dataset_pid'))
    def on_get(self, req, resp):
        file_id = req.params['file_id']
        dataset_pid = req.params['dataset_pid']

        # dv_file = self.dataverse_client.get_datafile_metadata(file_id)
        # if dv_file.status_code != 200:
        #     raise falcon.HTTPBadRequest('Dataverse returned an error', dv_file.text)
        #
        # dv_file_dict = json.loads(dv_file.text)

        dv_dataset = self.dataverse_client.get_dataset(dataset_pid)
        if dv_dataset.status_code != 200:
            raise falcon.HTTPBadRequest('Dataverse returned an error', dv_dataset.text)
        dv_dataset_dict = json.loads(dv_dataset.content.decode("utf-8"))['data']

        file_metadata = next(
            item for item in dv_dataset_dict['latestVersion']['files'] if str(item['dataFile']['id']) == file_id)
        filename = file_metadata['dataFile']['filename']
        filepath = os.path.join(dv_dataset_dict['storageIdentifier'][7:], filename)
        tmp_filepath = os.path.join(settings.TEMP_DIR, filepath)

        DataverseFileClient(self.dataverse_client).save_from(file_id=file_id, destination=tmp_filepath)

        resp.body = filepath
