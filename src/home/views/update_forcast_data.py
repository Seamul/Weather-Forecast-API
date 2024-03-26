from rest_framework.views import APIView
from rest_framework.response import Response
from ..tasks import run_forecast_update


class UpdateForcastData(APIView):
    """
    APIView class for updating forecast data for districts.

    Methods:
    - get: Handles GET requests to update forecast data.
    """

    def get(self, request):
        """
        Handles GET requests to update forecast data.

        Returns:
        - Response: JSON response indicating success or failure.
        """
        
        task = run_forecast_update.delay()
        return Response({"message": "Forecast data update started. Please wait while the update completes. You can see the status in the terminal."})

