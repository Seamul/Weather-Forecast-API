from home.models import District
from home.serializer import DistrictSerializer

class DistrictDataRetriever:
    """
    Singleton class for retrieving districts data from the database.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Initialization code here

    def get_districts_data(self):
        """
        Retrieves districts data from the database.

        Returns:
        - list: List of district data.
        """
        districts = District.objects.all()
        return DistrictSerializer(districts, many=True).data


