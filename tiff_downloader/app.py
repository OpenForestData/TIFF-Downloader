import falcon
from pyDataverse.api import Api

from . import settings
from .views import Uploader


def create_app(dataverse_client):
    api = falcon.API()

    # routing
    api.add_route('/tiff', Uploader(dataverse_client))
    return api


def get_app():
    dataverse_client = Api(base_url=settings.DATAVERSE_URL, api_token=settings.DATAVERSE_API_TOKEN)
    return create_app(dataverse_client)
