""" Utility functions for the AWC API. """

import json
import re
import requests
from . import const
from types import NoneType

def is_valid_icao(icao_code: list) -> bool:
    """ Validates the given ICAO IDs. """
    if len(icao_code) != 4:
        print(f"ICAO ID must be 4 characters long. {icao_code} is invalid.")
        return False
    if icao_code[0].upper() not in ["K", "P"]:
        print(f"ICAO ID must start with K. {icao_code} is invalid.")
        return False
    pattern = r"[^a-zA-Z0-9]" #Define valid characters for ICAO IDs and comma separator
    matches = re.findall(pattern, icao_code)
    if len(matches) > 0:
        print(f"Error in {icao_code}: ICAO ID must contain only letters and numbers.")
        return False
    return True

def is_valid_cwa(cwa: str) -> bool:
    """ Validates the given CWA. """
    if len(cwa) != 4:
        print(f"CWA must be 4 characters long. {cwa} is invalid.")
        return False
    pattern = r"[^a-zA-Z]" #Define valid characters for CWA
    matches = re.findall(pattern, cwa)
    if len(matches) > 0:
        print(f"Error in {cwa}: CWA must contain only letters.")
        return False
    return True

def icao_str_from_list(icao_list: list) -> str:
    """ Converts the given list of ICAO IDs to a string. """
    icao_list.sort()
    for icao_code in icao_list:
        if not is_valid_icao(icao_code):
            icao_list.remove(icao_code)
    icao_str = ",".join(icao_list)
    return icao_str.upper()

def fetch_forecast_discussion(cwa: str, aviation_only: bool = False, bypass_cwa_verification: bool = False) -> str:
    """ Fetches the forecast discussion for the given ICAO ID. """
    if not bypass_cwa_verification:
        if not is_valid_cwa(cwa):
            return None

    if aviation_only:
        discussion_type = "afd"
    else:
        discussion_type = "af"

    url = f"{const.API_BASE_URL}fcstdisc?cwa={cwa}&type={discussion_type}"
    print(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.text == const.NO_AFD_DATA_STR:
            return None
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching Forecast Discussion Data: {e}")
        return None

def fetch_metar(airport_list: list) -> dict:
    """ Fetches the METAR data for the given ICAO ID. """

    icao_ids = icao_str_from_list(airport_list)
    url = f"{const.API_BASE_URL}metar?ids={icao_ids}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        if len(response.text) > 2:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"Error fetching METAR data: {e}")
        return None

def fetch_taf(airport_list: list) -> dict:
    """ Fetches the TAF data for the given ICAO ID. """
    icao_ids = icao_str_from_list(airport_list)
    url = f"{const.API_BASE_URL}taf?ids={icao_ids}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        if len(response.text) > 2:
            return response.json()
        return None
    except requests.RequestException as e:
        print(f"Error fetching METAR data: {e}")
        return None

def save_json(data: dict, filename: str) -> None:
    """ Saves the given data to a JSON file. """
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {filename}.")
    except IOError as e:
        print(f"Error saving data to file: {e}")

def save_text(data: str, filename: str) -> None:
    """ Saves the given data to a text file. """
    if type(data) != str:
        if type(data) == NoneType:
            print("No data to save.")
            return
        else:
            print(f"Data must be a string. {type(data)} is invalid.")
    
    try:
        with open(filename, 'w', encoding='utf-8') as text_file:
            text_file.write(data)
    except Exception as e:
        print(f"Error saving data to file: {e}")

if __name__ == "__main__":
    airports = ["KJFK", "KORD", "KATL"]
    metar_data = fetch_metar(airports)
    taf_data = fetch_taf(airports)
    save_json(metar_data, "metar.json")
    save_json(taf_data, "taf.json")

#EOF
