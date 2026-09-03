# API stuff is here:
# "https://wcc.sc.egov.usda.gov/awdbRestApi/swagger-ui/index.html#/Data/getData"

# libraries, imports
from pathlib import Path

import requests
import pandas as pd

# project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_SCAN_DIR = PROJECT_ROOT / "data" / "raw" / "scan"
STATIONS_FILE = RAW_SCAN_DIR / "scan_stations.csv"

RAW_SCAN_DIR.mkdir(exist_ok=True, parents=True)
if not STATIONS_FILE.exists():
    STATIONS_FILE.touch()

# the urls 
AWDB_BASE_URL = ("https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1")
STATIONS_ENDPOINT = f"{AWDB_BASE_URL}/stations"
STATIONS_ENDPOINT = f"{AWDB_BASE_URL}/stations"
DATA_ENDPOINT = f"{AWDB_BASE_URL}/data"

# get STATION DATA from their APIs (need to see if it'll work)
def get_scan_stations():
    """
    Get SCAN stations' metadata from USDA NRCS AwDB REST API
    Returns:
        pandas dataframe of station metadata I think
    """

    params = {
        "stationTriplets": "*:*:SCAN",
        "elements": "SMS:*",
        "activeOnly": "false",
    }

    response = requests.get(STATIONS_ENDPOINT, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data=data)

# save STATION DATA
def save_scan_stations(stations):
    """
    Just save the ones we got
    """
    RAW_SCAN_DIR.mkdir(exist_ok=True, parents=True)
    if not STATIONS_FILE.exists():
        STATIONS_FILE.touch()

    stations.to_csv(STATIONS_FILE, index=False)

    print(f"Saved {len(stations)} stations to:")
    print(STATIONS_FILE)

# now ONE STATION'S INNER DATA, daily for now
def _get_scan_data(station_triplet, elements="SMS:*", duration="DAILY", begin_date=None, end_date=None):
    """
    Retrieve SCAN observations for one station

    Returns the raw JSON response from the AWDB API
    """

    params = {
        "stationTriplets": station_triplet,
        "elements": elements,
        "duration": duration,
        "periodRef": "END",
        "returnFlags": "true",
        "returnOriginalValues": "false",
        "returnSuspectData": "false",
    }

    if begin_date is not None:
        params["beginDate"] = begin_date

    if end_date is not None:
        params["endDate"] = end_date

    response = requests.get(DATA_ENDPOINT, params=params, timeout=60)
    response.raise_for_status()

    return response.json()

# convert stuff from JSON to DF
def _parse_scan_response(raw_response):
    records = []

    if not raw_response:
        return pd.DataFrame(
            columns=[
                "date",
                "element",
                "depth_inches",
                "value",
                "qc_flag",
                "qa_flag",
            ]
        )

    for element_data in raw_response[0]["data"]:
        element = element_data["stationElement"]

        for obs in element_data["values"]:
            records.append({
                "date": obs["date"],
                "element": element["elementCode"],
                "depth_inches": element["heightDepth"],
                "value": obs.get("value"),
                "qc_flag": obs.get("qcFlag"),
                "qa_flag": obs.get("qaFlag"),
            })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])

    return df.sort_values(["date", "depth_inches"]).reset_index(drop=True)

# download long histories in smaller chunks
def download_scan_history(
    station_triplet,
    start_year=1980,
    end_year=2026,
    chunk_years=5,
):
    all_data = []

    # break years up into chunk year intervals so no server limits
    for year in range(start_year, end_year + 1, chunk_years):
        chunk_start = year
        chunk_end = min(year + chunk_years - 1, end_year)

        raw_data = _get_scan_data(
            station_triplet=station_triplet,
            elements="SMS:*",
            duration="DAILY",
            begin_date=f"{chunk_start}-01-01",
            end_date=f"{chunk_end}-12-31",
        )

        all_data.append(_parse_scan_response(raw_data))

    return pd.concat(all_data, ignore_index=True)

