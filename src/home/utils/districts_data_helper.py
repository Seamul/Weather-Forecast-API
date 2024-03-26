from home.models import District
from home.serializer import DistrictSerializer


def get_districts_data():
    """
    Retrieves districts data from the database.

    Returns:
    - list: List of district data.
    """
    districts = District.objects.all()
    return DistrictSerializer(districts, many=True).data
