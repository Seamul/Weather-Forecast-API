

from celery import shared_task

from home.utils.forecast_update_helper import ForecastUpdateCommand
from home.utils.districts_data_helper import get_districts_data


@shared_task(bind=True)
def run_forecast_update(self):
    """
    Orchestrates the workflow to update forecast data.
    """
    print("==============Initiated forecast data update process===================")
    districts_data = get_districts_data()
    forecast_update_command = ForecastUpdateCommand(districts_data)
    forecast_update_command.execute()
    print("=================Forecast data update process completed=================")
    return "Forecast data updated successfully"
