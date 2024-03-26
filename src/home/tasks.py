

from celery import shared_task

from home.utils.forecast_update_helper import get_districts_data, ForecastUpdateCommand


@shared_task(bind=True)
def run_forecast_update(self):
    """
    Orchestrates the workflow to update forecast data.
    """
    print("--------------start updating forecast data------------")
    districts_data = get_districts_data()
    forecast_update_command = ForecastUpdateCommand(districts_data)
    forecast_update_command.execute()
    print("---------updated forecast data--------")
    return "Forecast data updated successfully"
