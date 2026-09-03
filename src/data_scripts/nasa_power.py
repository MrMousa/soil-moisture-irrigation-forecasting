# API stuff is here:
# https://power.larc.nasa.gov/docs/services/api/

# libraries, imports
import requests
import pandas as pd

# API url
POWER_ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"


# get weather data from their API
def get_nasa_power_data(latitude, longitude, start_date, end_date):
    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON",
    }

    response = requests.get(POWER_ENDPOINT, params=params, timeout=60)
    response.raise_for_status()

    return response.json()


# convert their JSON into a normal dataframe
def parse_nasa_power_response(raw_response):
    data = raw_response["properties"]["parameter"]

    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"

    return df.reset_index()