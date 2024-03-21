from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from ..models import ForecastData

class CompareTemperature(APIView):
    def post(self, request):
        # Get data from request
        long1 = request.data.get('long1')
        lat1 = request.data.get('lat1')
        long2 = request.data.get('long2')
        lat2 = request.data.get('lat2')
        travel_date_str = request.data.get('travel_date')


        location1 = (long1, lat1)  # Dhaka
        location2 = (long2, lat2)

        # Parse travel date
        # date = datetime.strptime(travel_date_str, "%Y-%m-%d")

        # Return the decision in the API response
        return Response({"decision": "decision"})

