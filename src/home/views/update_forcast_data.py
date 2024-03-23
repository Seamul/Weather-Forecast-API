"""
Module: update_forecast_data.py

This module contains an APIView class, UpdateForcastData, for updating forecast data for districts.

Classes:
- UpdateForcastData: APIView class for updating forecast data.

Functions:
- delete_existing_forecast_data: Deletes existing forecast data from the database.
- get_districts_data: Retrieves districts data from the database.
- get_or_create_forecast_meta_data: Retrieves or creates forecast metadata for a district.
- save_weather_data: Saves weather data for a district.

Dependencies:
- Django
- Django Rest Framework
- requests_cache
- retry_requests
- home.utils.help_file: OpenMeteoApiClient, WeatherDataFactory
- home.models: District, ForecastData, ForecastMetaData
- home.serializer: DistrictSerializer
- datetime

Usage:
- Import UpdateForcastData class and call its get method to update forecast data.

API Endpoint:
- URL: GET http://0.0.0.0:8700/api/update_forcast_data/
- Method: GET
- Response:
    {
        "message": "Forecast data saved successfully"
    }
"""

from rest_framework.views import APIView
from rest_framework.response import Response
import requests_cache
from retry_requests import retry
from home.utils.help_file import OpenMeteoApiClient, WeatherDataFactory
from home.models import District, ForecastData, ForecastMetaData
from home.serializer import DistrictSerializer
from datetime import datetime
from django.core.cache import cache


class UpdateForcastData(APIView):
    """
    APIView class for updating forecast data for districts.

    Methods:
    - get: Handles GET requests to update forecast data.
    - delete_existing_forecast_data: Deletes existing forecast data from the database.
    - get_districts_data: Retrieves districts data from the database.
    - get_or_create_forecast_meta_data: Retrieves or creates forecast metadata for a district.
    - save_weather_data: Saves weather data for a district.
    """

    def get(self, request):
        """
        Handles GET requests to update forecast data.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        self.delete_existing_forecast_data()

        districts_data = self.get_districts_data()

        # Set up caching and retrying mechanisms
        cache_session = requests_cache.CachedSession(
            '.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        # Create the weather API client and data factory
        openmeteo_api_client = OpenMeteoApiClient(session=retry_session)
        weather_data_factory = WeatherDataFactory(
            api_client=openmeteo_api_client)

        # Loop through districts and fetch weather data
        for district_data in districts_data:
            forecast_meta_data = self.get_or_create_forecast_meta_data(
                district_data)
            self.save_weather_data(weather_data_factory, forecast_meta_data)

        return Response({"message": "Forecast data saved successfully"})

    def delete_existing_forecast_data(self):
        """
        Deletes existing forecast data from the database.
        """
        ForecastData.objects.all().delete()
        ForecastMetaData.objects.all().delete()
        cache.clear()

    def get_districts_data(self):
        """
        Retrieves districts data from the database.

        Returns:
        - list: List of district data.
        """
        districts = District.objects.all()
        return DistrictSerializer(districts, many=True).data

    def get_or_create_forecast_meta_data(self, district_data):
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

    def save_weather_data(self, weather_data_factory, forecast_meta_data):
        """
        Saves weather data for a district.

        Args:
        - weather_data_factory (WeatherDataFactory): Weather data factory instance.
        - forecast_meta_data (ForecastMetaData): Forecast metadata instance.
        """
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
