from celery import shared_task
from django.db import transaction
from home.utils.forecast_update_helper import ForecastUpdateCommand
from home.utils.districts_data_helper import DistrictDataRetriever

@shared_task(bind=True)
def run_forecast_update(self, forecast_url):
    """
    Task to update forecast data.
    
    Args:
    - forecast_url (str): The URL from which to fetch the forecast data.
    
    Returns:
    - str: A message indicating the status of the forecast data update.
    """
    with transaction.atomic():
        print("==============Initiated forecast data update process===================")
        
        # Retrieve district data
        district_retriever = DistrictDataRetriever()
        districts_data = district_retriever.get_districts_data()
        
        # Execute forecast update command
        forecast_update_command = ForecastUpdateCommand(districts_data, forecast_url)
        forecast_update_command.execute()
        
        print("=================Forecast data update process completed=================")
        
        return "Forecast data updated successfully"
