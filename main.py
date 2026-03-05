#https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
#OR https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=f489f1e802cce582d5c27a29bd3911cf

#https://jsonviewer.stack.hu/
#https://www.ventusky.com/#p=46.6;13.4;5
#https://console.twilio.com/?overrideTreatment=post-signup-dev&selectedTab=dynamic

import requests
import pandas as pd

def get_coordinates(city):
    url = f"http://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url).json()

    if "results" in response:
        lat = response["results"][0]["latitude"]
        lon = response["results"][0]["longitude"]
        print(f"{city} is located at: {lat}, {lon}")
    else:
        print("City not found.")
    return (lat, lon)

def get_weather_meteo(city):
    (lat, lon) = get_coordinates(city)

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "weather_code", "wind_speed_10m", "wind_gusts_10m", "surface_pressure",
                   "relative_humidity_2m", "apparent_temperature", "rain", "showers", "snowfall", "visibility",
                   "precipitation", "cloud_cover", "wind_direction_10m", "uv_index"],
        "forecast_days": 1,
        "temporal_resolution": "hourly_3",
    }

    response_obj = requests.get("http://api.open-meteo.com/v1/forecast", params=params)
    response_obj.raise_for_status()

    response = response_obj.json()
    print(response)

    # Process first location. Add a for-loop for multiple locations or weather models
    #response = response[0]
    print(f"Coordinates: {response['latitude']}°N {response['longitude']}°E")
    print(f"Elevation: {response['elevation']} m asl")
    print(f"Timezone difference to GMT+0: {response['utc_offset_seconds']}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response['hourly']
    hourly_temperature_2m = hourly['temperature_2m']
    hourly_weather_code = hourly['weather_code']
    hourly_wind_speed_10m = hourly['wind_speed_10m']
    hourly_wind_gusts_10m = hourly['wind_gusts_10m']
    hourly_surface_pressure = hourly['surface_pressure']
    hourly_relative_humidity_2m = hourly['relative_humidity_2m']
    hourly_apparent_temperature = hourly['apparent_temperature']
    hourly_rain = hourly['rain']
    hourly_showers = hourly['showers']
    hourly_snowfall = hourly['snowfall']
    hourly_visibility = hourly['visibility']
    hourly_precipitation = hourly['precipitation']
    hourly_cloud_cover = hourly['cloud_cover']
    hourly_wind_direction_10m = hourly['wind_direction_10m']
    hourly_uv_index = hourly['uv_index']


def get_weather_openweathermap(city):
#https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=f489f1e802cce582d5c27a29bd3911cf
    params = {
        'appid':'f489f1e802cce582d5c27a29bd3911cf',
        'q':city,
        'units':'metric',
        'cnt':4
    }

    #response_obj = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)
    response_obj = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=params)
    response_obj.raise_for_status()

    response = response_obj.json()
    #print(response)
    return response

def get_weather_ids(resp):
    ret = []
    for hour_data in resp["list"]:
        ret.append(hour_data["weather"][0]["id"])
    return ret

def check_weather_ids(ids):
    x=""
    for i in ids:
        if int(i)<700:
            x="Bring an umbrella!"
    print(x)



#MAIN
#get_weather_meteo("Vienna")
r=get_weather_openweathermap("London")
ids=get_weather_ids(r)
check_weather_ids(ids)
