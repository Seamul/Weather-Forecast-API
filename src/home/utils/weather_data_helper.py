import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from abc import ABC, abstractmethod


class WeatherApiClient(ABC):
    """
    Abstract base class for weather API clients.

    This class defines the interface for weather API clients, requiring implementation of the get_weather_data method.

    Attributes:
    - session: Session object used for making HTTP requests to the weather API.
    """

    def __init__(self, session):
        """
        Initializes the WeatherApiClient with a session object.

        Args:
        - session: Session object for making HTTP requests.
        """
        self.session = session

    @abstractmethod
    def get_weather_data(self, forecast_url, latitude, longitude, location_name):
        """
        Abstract method to retrieve weather data for a given location.

        Args:
        - forecast_url (str): The URL for fetching forecast data.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - location_name (str): Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
        pass


class OpenMeteoApiClient(WeatherApiClient):
    """
    Weather API client for Open-Meteo service.

    This class implements the WeatherApiClient interface for interacting with the Open-Meteo API.

    Attributes:
    - session: Session object used for making HTTP requests to the weather API.
    """

    def get_weather_data(self, forecast_url, latitude, longitude, location_name):
        """
        Retrieves weather data for a given location from the Open-Meteo API.

        Args:
        - forecast_url (str): The URL for fetching forecast data.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - location_name (str): Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(forecast_url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]

        # Process hourly data
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
    """
    Factory class for retrieving weather data using a specified API client.

    This class provides a single method to retrieve weather data for a given location using the configured API client.

    Attributes:
    - forecast_url (str): The URL for fetching forecast data.
    - api_client: Weather API client instance.
    """

    def __init__(self, forecast_url, api_client):
        """
        Initializes the WeatherDataFactory with a forecast URL and an API client.

        Args:
        - forecast_url (str): The URL for fetching forecast data.
        - api_client: Weather API client instance.
        """
        self.forecast_url = forecast_url
        self.api_client = api_client

    def get_weather_data(self, latitude, longitude, location_name):
        """
        Retrieves weather data for a given location using the configured API client.

        Args:
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
        - location_name (str): Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
        return self.api_client.get_weather_data(self.forecast_url, latitude, longitude, location_name)
