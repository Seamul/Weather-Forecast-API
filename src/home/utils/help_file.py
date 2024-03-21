import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from abc import ABC, abstractclassmethod


class WeatherApiClient(ABC):
    def __init__(self, session):
        self.session = session

    @abstractclassmethod
    def get_weather_data(self, latitude, longitude, location_name):
        pass


class OpenMeteoApiClient(WeatherApiClient):
    def get_weather_data(self, latitude, longitude, location_name):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession(
            '.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(
            f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "latitude": latitude,
            "longitude": longitude,
            "location_name": location_name,
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_2m": hourly_temperature_2m.tolist(),
        }

        return hourly_data


class WeatherDataFactory:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_weather_data(self, latitude, longitude, location_name):
        return self.api_client.get_weather_data(latitude, longitude, location_name)
