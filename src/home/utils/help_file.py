"""
Module: openmeteo_requests.py

This module provides classes for interacting with weather APIs to retrieve weather data.

Classes:
- WeatherApiClient: Abstract base class for weather API clients.
- OpenMeteoApiClient: Weather API client for Open-Meteo service.
- WeatherDataFactory: Factory class for retrieving weather data using a specified API client.

Dependencies:
- openmeteo_requests (custom module)
- requests_cache
- pandas
- retry_requests
- abc (Abstract Base Classes)

Usage:
- Import WeatherApiClient, OpenMeteoApiClient, and WeatherDataFactory classes as needed.
- Instantiate WeatherDataFactory with a suitable API client to retrieve weather data.

Example:
    # Instantiate OpenMeteoApiClient
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo_api_client = OpenMeteoApiClient(session=retry_session)

    # Instantiate WeatherDataFactory with OpenMeteoApiClient
    weather_data_factory = WeatherDataFactory(api_client=openmeteo_api_client)

    # Use WeatherDataFactory to get weather data
    latitude = 52.52
    longitude = 13.405
    location_name = "Berlin"
    weather_data = weather_data_factory.get_weather_data(latitude, longitude, location_name)

    # Use the weather data as needed
    print(weather_data)

API Classes:
1. WeatherApiClient:
    - Abstract base class defining the interface for weather API clients.
    - Requires implementation of the get_weather_data method.

2. OpenMeteoApiClient(WeatherApiClient):
    - Concrete implementation of WeatherApiClient for interacting with the Open-Meteo API.
    - Retrieves weather data for a given latitude, longitude, and location name.

3. WeatherDataFactory:
    - Factory class for retrieving weather data using a specified API client.
    - Provides a single method, get_weather_data, to retrieve weather data.

Methods:
- get_weather_data(latitude, longitude, location_name):
    - Retrieves weather data for the specified location from the configured weather API.

Attributes:
- session: Session object used for making HTTP requests to the weather API.

"""

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from abc import ABC, abstractclassmethod


class WeatherApiClient(ABC):
    """
    Abstract base class for weather API clients.

    Methods:
    - get_weather_data: Abstract method to retrieve weather data.
    """

    def __init__(self, session):
        """
        Initializes the WeatherApiClient with a session object.

        Args:
        - session: Session object for making HTTP requests.
        """
        self.session = session

    @abstractclassmethod
    def get_weather_data(self, latitude, longitude, location_name):
        """
        Abstract method to retrieve weather data for a given location.

        Args:
        - latitude: Latitude of the location.
        - longitude: Longitude of the location.
        - location_name: Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
        pass


class OpenMeteoApiClient(WeatherApiClient):
    """
    Weather API client for Open-Meteo service.

    Methods:
    - get_weather_data: Retrieves weather data from the Open-Meteo API.
    """

    def get_weather_data(self, latitude, longitude, location_name):
        """
        Retrieves weather data for a given location from the Open-Meteo API.

        Args:
        - latitude: Latitude of the location.
        - longitude: Longitude of the location.
        - location_name: Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
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
    """
    Factory class for retrieving weather data using a specified API client.

    Methods:
    - get_weather_data: Retrieves weather data for a given location using the configured API client.
    """

    def __init__(self, api_client):
        """
        Initializes the WeatherDataFactory with an API client.

        Args:
        - api_client: Weather API client instance.
        """
        self.api_client = api_client

    def get_weather_data(self, latitude, longitude, location_name):
        """
        Retrieves weather data for a given location using the configured API client.

        Args:
        - latitude: Latitude of the location.
        - longitude: Longitude of the location.
        - location_name: Name of the location.

        Returns:
        - dict: Weather data for the location.
        """
        return self.api_client.get_weather_data(latitude, longitude, location_name)
