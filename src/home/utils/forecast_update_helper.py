import requests_cache
from retry_requests import retry
from home.utils.weather_data_helper import OpenMeteoApiClient, WeatherDataFactory
from home.models import ForecastData, ForecastMetaData

from datetime import datetime
from django.core.cache import cache


class ForecastUpdateCommand:
    """
    Class to execute the forecast update command.

    This class orchestrates the process of updating forecast data for districts.

    Attributes:
    - districts_data (list): List of district data.
    - forecast_url (str): URL to fetch forecast data.
    """

    def __init__(self, districts_data, forecast_url):
        """
        Initializes the ForecastUpdateCommand with districts_data and forecast_url.

        Args:
        - districts_data (list): List of district data.
        - forecast_url (str): URL to fetch forecast data.
        """
        self.districts_data = districts_data
        self.forecast_url = forecast_url

    def execute(self):
        """
        Executes the forecast update command.

        This method fetches weather data for each district,
        saves it to the database, and clears the cache.
        """
        self._delete_existing_forecast_data()
        self._fetch_and_save_weather_data()

    def _delete_existing_forecast_data(self):
        """
        Deletes existing forecast data from the database.
        """
        ForecastData.objects.all().delete()
        ForecastMetaData.objects.all().delete()
        cache.clear()

    def _fetch_and_save_weather_data(self):
        """
        Fetches weather data for each district and saves it to the database.
        """
        for district_data in self.districts_data:
            forecast_meta_data = self._get_or_create_forecast_meta_data(district_data)
            self._save_weather_data(forecast_meta_data)

    def _get_or_create_forecast_meta_data(self, district_data):
        """
        Retrieves or creates forecast metadata for a district.

        Args:
        - district_data (dict): District data.

        Returns:
        - ForecastMetaData: Forecast metadata instance.
        """
        latitude = float(district_data['lat'])
        longitude = float(district_data['long'])
        name = district_data['name']
        return ForecastMetaData.objects.get_or_create(
            latitude=latitude, longitude=longitude, location_name=name
        )[0]

    def _save_weather_data(self, forecast_meta_data):
        """
        Saves weather data for a district.

        Args:
        - forecast_meta_data (ForecastMetaData): Forecast metadata instance.
        """
        weather_data_factory = WeatherDataFactory(self.forecast_url, OpenMeteoApiClient(session=self._get_retry_session()))
        weather_data = weather_data_factory.get_weather_data(
            float(forecast_meta_data.latitude),
            float(forecast_meta_data.longitude),
            forecast_meta_data.location_name
        )

        date_list = weather_data["date"]
        temperature_list = weather_data["temperature_2m"]
        average_temperature = sum(temperature_list) / len(temperature_list)
        forecast_meta_data.average_temperature = average_temperature
        forecast_meta_data.save()

        for date_str, temperature in zip(date_list, temperature_list):
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            ForecastData.objects.create(
                forecast_meta_data=forecast_meta_data,
                date=date,
                temperature_2m=float(temperature),
            )

    def _get_retry_session(self):
        """
        Returns a retry-enabled session for making API requests.

        Returns:
        - requests.Session: Retry-enabled session.
        """
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        return retry(cache_session, retries=5, backoff_factor=0.2)
