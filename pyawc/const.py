"""
Constants used in the pyawc package.
"""

import os
from typing import Final

file_dir = os.path.join(os.path.dirname(__file__), "..")

API_BASE_URL: Final[str] = "https://aviationweather.gov/api/data/"
API_METAR_URL: Final[str] = "metar?ids={}&format=json&taf={}"
API_TAF_URL: Final[str] = "taf?ids={}&format=json"

DEFAULT_USERID: Final[str] = "CODEemail@address"

NO_AFD_DATA_STR: Final[str] = "No AFD Data Available"

ALERT_ID: Final[str] = "id"
