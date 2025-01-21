"""Example script to demonstrate the usage of the pyawc library."""

from pyawc import fetch_metar, fetch_taf, save_text, save_json, fetch_forecast_discussion
from tqdm import tqdm
from time import sleep

def FetchAllDiscussions(stations):
    """ Fetches forecast discussions for all stations in the given list. """
    successful_grabs = []
    failed_grabs = []
    discussion_dict = {}
    consequent_urls = 0
    for icao in tqdm(stations, desc="Fetching discussions"):
        if consequent_urls < 10:
            discussion = fetch_forecast_discussion(icao, aviation_only=False, bypass_cwa_verification=True)
            consequent_urls += 1
        else:
            sleep(1)
            consequent_urls = 0
            discussion = fetch_forecast_discussion(icao, aviation_only=False, bypass_cwa_verification=True)
        if discussion:
            discussion_dict[icao] = discussion
            successful_grabs.append(icao)
        else:
            failed_grabs.append(icao)
    save_json(discussion_dict, "discussions.json")
    print(f"Successfully grabbed forecast discussions for {len(successful_grabs)}/{len(stations)} airports.")

def main():
    """ Main function to demonstrate the usage of the pyawc library. """
    with open("us_airport_codes.txt") as f:
        airport_list = f.read().splitlines()

    with open("us_cwas.txt") as f:
        cwa_list = f.read().splitlines()
    #save_json(fetch_metar(airport_list), "metars.json")
    #save_json(fetch_taf(airport_list), "tafs.json")
    FetchAllDiscussions(cwa_list[:1])
    
if __name__ == "__main__":
    main()
#EOF