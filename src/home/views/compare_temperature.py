"""
Module: compare_temperature.py

This module contains an APIView class, CompareTemperature, for comparing temperatures between present and destination locations.

Classes:
- CompareTemperature: APIView class for comparing temperatures.

Dependencies:
- Django
- Django Rest Framework
- datetime
- ..models: ForecastData, ForecastMetaData

Usage:
- Import CompareTemperature class and call its post method to compare temperatures between present and destination locations.

Example API Call:
POST http://0.0.0.0:8700/api/compare_temperature/
Request Body:
{
  "present_location": "Dhaka",
  "destination_location": "Gopalganj",
  "travel_date": "2024-03-26"
}

Response:
{
    "Decision": "Your destination 'Gopalganj' has a cooler temperature (24.5°C) compared to present_location 'Dhaka' (28.3°C). It's suitable for travel. You should travel there"
}
"""

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models import ForecastData, ForecastMetaData


class CompareTemperature(APIView):
    """
    APIView class for comparing temperatures between present and destination locations.

    Methods:
    - post: Handles POST requests to compare temperatures.
    """

    def post(self, request):
        """
        Handles POST requests to compare temperatures.

        Args:
        - request (Request): HTTP request object containing present_location, destination_location, and travel_date.

        Returns:
        - Response: JSON response indicating the comparison decision.
        """
        present_location = request.data.get('present_location')
        destination_location = request.data.get('destination_location')

        cache_key = f"compare_temperature_{present_location}_{destination_location}"

        # Check if data exists in cache
        cached_response = cache.get(cache_key)
        if cached_response:
            # Check if request data matches cached data
            if cached_response.get('request_data') == request.data:
                cached_response['response_data']['source'] = 'cache'
                return Response(cached_response['response_data'])

        try:
            present_location_obj = ForecastMetaData.objects.get(
                location_name=present_location)
            destination_location_obj = ForecastMetaData.objects.get(
                location_name=destination_location)
        except ForecastMetaData.DoesNotExist:
            return Response({"error": f"One or both of the provided locations do not exist."}, status=status.HTTP_404_NOT_FOUND)

        travel_date = request.data.get('travel_date')

        travel_datetime = datetime.strptime(travel_date, "%Y-%m-%d")
        travel_datetime = travel_datetime.replace(
            hour=14)  # Set the time to 14:00:00

        try:
            present_forecast_data = ForecastData.objects.get(
                forecast_meta_data=present_location_obj, date=travel_datetime)
            destination_forecast_data = ForecastData.objects.get(
                forecast_meta_data=destination_location_obj, date=travel_datetime)
        except ForecastData.DoesNotExist:
            return Response({"error": f"No forecast data available for the specified date."}, status=status.HTTP_404_NOT_FOUND)

        if present_forecast_data.temperature_2m > destination_forecast_data.temperature_2m:
            decision = f'''Your destination '{destination_location}' has a cooler temperature ({destination_forecast_data.temperature_2m}°C) compared to present_location '{present_location}' ({present_forecast_data.temperature_2m}°C). It's suitable for travel. You should travel there'''
        else:
            decision = f'''Your destination '{destination_location}' does not have a cooler temperature ({destination_forecast_data.temperature_2m}°C) compared to present_location '{present_location}' ({present_forecast_data.temperature_2m}°C). It's not suitable for travel. You should not travel there'''

        response_data = {"Decision": decision, "source": "database"}

        # Cache the response along with request data
        cache.set(cache_key, {'request_data': request.data, 'response_data': response_data}, 60 * 15)  # Cache for 15 minutes

        return Response(response_data)

