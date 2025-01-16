""" Main module for pyawc package. """
from pyawc import fetch_metar, fetch_taf, save_json, fetch_forecast_discussion

def FetchAllTafs(stations):
    successful_grabs = []
    failed_grabs = []
    discussion_dict = {}
    for icao in stations:
        discussion = fetch_forecast_discussion(icao, True)
        if discussion:
            discussion_dict[icao] = discussion
            successful_grabs.append(icao)
        else:
            failed_grabs.append(icao)
    save_json(discussion_dict, "discussions.json")
    print(f"Successfully grabbed forecast discussions for {len(successful_grabs)} airports.")

airport_list = [
    "KATL", "KORD", "KJFK", "KSEA", "KLAX", "KDFW", "KMIA", "KSFO", "KDEN", "PHNL",
    "KPHX", "KIAH", "KDTW", "KMCO", "KCLT", "KSLC", "KPDX", "KSJC", "KBOS", "KMSY",
    "KMEM", "KMSP", "KTPA", "KMDW", "KAUS", "KBNA", "KDAL", "KPIT", "KSTL", "KIND",
    "KCVG", "KCMH", "KCLE", "KBDL", "KJAX", "KRIC", "KBUF", "KOKC", "KOMA", "KPHL",
    "KSAN", "KSMF", "KABQ", "KBWI", "KELP", "KORF", "KALB", "KROC", "KSYR", "KDAY",
    "KDSM", "KBOI"
]

save_json(fetch_metar(airport_list), "metars.json")
save_json(fetch_taf(airport_list), "tafs.json")
FetchAllTafs(airport_list)