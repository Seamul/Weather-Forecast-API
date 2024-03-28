"""
API Endpoint: /api/update_forecast_data/

This endpoint triggers the update of forecast data for districts.

Request Method: POST

Request Body:
{
    "forecast_url": "string"  # The URL of the forecast data to be updated
}

Example:
{
    "forecast_url":"https://api.open-meteo.com/v1/forecast"
}

Response:
- 200 OK: {
    "message": "Forecast data update started. Please wait while the update completes. You can see the status in the terminal."
}
- 400 Bad Request: {
    "error": "Forecast URL is missing. Please provide a forecast URL."
}
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..tasks import run_forecast_update

class UpdateForecastData(APIView):
    """
    APIView class for updating forecast data for districts.

    Attributes:
    - run_forecast_update: Celery task for updating forecast data.
    """

    def post(self, request):
        """
        Handles POST requests to update forecast data.

        This method initiates a Celery task to update forecast data for districts.

        Args:
        - request (Request): POST request object containing the forecast URL.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        request_data = request.data.copy()
        forecast_url = request_data.get('forecast_url')

        if forecast_url:
            # Initiate Celery task to update forecast data
            task = run_forecast_update.delay(forecast_url)
            return Response({"message": "Forecast data update started. Please wait while the update completes. You can see the status in the terminal."})
        else:
            return Response({"error": "Forecast URL is missing. Please provide a forecast URL."}, status=status.HTTP_400_BAD_REQUEST)
