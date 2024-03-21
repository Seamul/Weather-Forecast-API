from rest_framework.views import APIView
from rest_framework.response import Response
import requests_cache
# import pandas as pd
from retry_requests import retry
from home.utils.help_file import OpenMeteoApiClient, WeatherDataFactory
from home.models import District, ForecastData, ForecastMetaData
from home.serializer import DistrictSerializer
from datetime import datetime
from datetime import datetime


class UpdateForcastData(APIView):
    def get(self, request):
        self.delete_existing_forecast_data()

        districts_data = self.get_districts_data()

        # Set up caching and retrying mechanisms
        cache_session = requests_cache.CachedSession(
            '.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        # Create the weather API client and data factory
        openmeteo_api_client = OpenMeteoApiClient(session=retry_session)

        # TODO: this is using from OOP
        weather_data_factory = WeatherDataFactory(
            api_client=openmeteo_api_client)

        # Loop through districts and fetch weather data
        for district_data in districts_data:
            # TODO: use only this method
            forecast_meta_data = self.get_or_create_forecast_meta_data(
                district_data)
            self.save_weather_data(weather_data_factory, forecast_meta_data)

        return Response({"message": "Forecast data saved successfully"})

    def delete_existing_forecast_data(self):
        ForecastData.objects.all().delete()
        ForecastMetaData.objects.all().delete()

    def get_districts_data(self):
        districts = District.objects.all()
        return DistrictSerializer(districts, many=True).data

    def get_or_create_forecast_meta_data(self, district_data):
        latitude = float(district_data['lat'])
        longitude = float(district_data['long'])
        name = district_data['name']
        return ForecastMetaData.objects.get_or_create(
            latitude=latitude, longitude=longitude, location_name=name
        )[0]

    def save_weather_data(self, weather_data_factory, forecast_meta_data):
        #  print(f"Fetching weather data for {name}...")
        weather_data = weather_data_factory.get_weather_data(
            float(forecast_meta_data.latitude),
            float(forecast_meta_data.longitude),
            forecast_meta_data.location_name)

        # Extract weather data lists
        date_list = weather_data["date"]
        temperature_list = weather_data["temperature_2m"]
        average_temperature = sum(temperature_list)/len(temperature_list)
        forecast_meta_data.average_temperature = average_temperature
        forecast_meta_data.save()

        # Save weather data to ForecastData model
        for date_str, temperature in zip(date_list, temperature_list):
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            ForecastData.objects.create(
                forecast_meta_data=forecast_meta_data,
                date=date,
                temperature_2m=float(temperature),
            )
