from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models import ForecastData, ForecastMetaData


class CompareTemperature(APIView):
    def post(self, request):
        present_location = request.data.get('present_location')
        destination_location = request.data.get('destination_location')

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

        return Response({"Decision": decision})
