

from celery import shared_task

from home.utils.forecast_update_helper import ForecastUpdateCommand
from home.utils.districts_data_helper import DistrictDataRetriever
from django.db import transaction

@shared_task(bind=True)
def run_forecast_update(self):
    """
    Orchestrates the workflow to update forecast data.
    """
    with transaction.atomic():
        print("==============Initiated forecast data update process===================")
        district_retriever = DistrictDataRetriever()
        districts_data = district_retriever.get_districts_data()
        forecast_update_command = ForecastUpdateCommand(districts_data)
        forecast_update_command.execute()
        print("=================Forecast data update process completed=================")
        return "Forecast data updated successfully"
