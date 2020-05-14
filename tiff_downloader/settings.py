import os
import tempfile
from pathlib import Path

if os.environ.get('READ_DOT_ENV'):
    from dotenv import load_dotenv
    load_dotenv()

APP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DATAVERSE_URL = os.environ.get('DATAVERSE_URL')
DATAVERSE_API_TOKEN = os.environ.get('DATAVERSE_API_TOKEN', None)

TIFF_SERVER_ROOT = os.path.join(APP_DIR, os.environ.get('TIFF_SERVER_ROOT'))
Path(TIFF_SERVER_ROOT).mkdir(parents=True, exist_ok=True)

TEMP_DIR = os.path.join(APP_DIR, os.environ.get('TEMP_DIR', tempfile.gettempdir()))
Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
