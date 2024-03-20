from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import TestModel


# class HelloWorld(APIView):
#     def get(self, request):
#         return Response({"message": "Hello, World!"})

#     def post(self, request):
#         # {
#         #     "message": "Hello, World!"
#         # }
#         request_data = request.data.copy()
#         TestModel.objects.create(test_field=request_data['message'])
#         return Response(request_data)
# import openmeteo_requests
import requests_cache
# import pandas as pd
from retry_requests import retry
import requests
from home.utils.logic import OpenMeteoApiClient, WeatherDataFactory
from home.models import District, ForecastData
from home.serializer import DistrictSerializer, ForecastDataSerializer
from datetime import datetime


class UpdateForcastData(APIView):
    def get(self, request):
        # Delete existing forecast data
        ForecastData.objects.all().delete()
        
        # Set up caching and retrying mechanisms
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

        # Create the weather API client and data factory
        openmeteo_api_client = OpenMeteoApiClient(session=retry_session)
        weather_data_factory = WeatherDataFactory(api_client=openmeteo_api_client)

        # Retrieve districts data
        districts = District.objects.all()
        districts_data = DistrictSerializer(districts, many=True).data

        # Loop through districts and fetch weather data
        for location in districts_data:
            latitude = float(location['lat'])
            longitude = float(location['long'])
            name = location['name']
            print(f"Fetching weather data for {name}...")
            weather_data = weather_data_factory.get_weather_data(latitude, longitude, name)

            # Extract weather data lists
            date_list = weather_data["date"]
            temperature_list = weather_data["temperature_2m"]

            # Save weather data to ForecastData model
            for date_str, temperature in zip(date_list, temperature_list):
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                ForecastData.objects.create(
                    date=date,
                    temperature_2m=str(temperature),
                    latitude=latitude,
                    longitude=longitude,
                    location_name=name,
                )

        return Response({"message": "Forecast data saved successfully"})
