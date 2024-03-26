

---

# Weather-Forecast-API


This Django project serves as an API for managing district information in Bangladesh, including weather forecast data.

## Introduction

This API provides endpoints to retrieve information about districts in Bangladesh, including their names, coordinates, and weather forecasts. It includes functionality to update forecast data periodically using Celery tasks, but for simplicity, we'll run it manually.

## Features

- Retrieve a list of all districts.
- Retrieve detailed information about a specific district.
- Access weather forecast data for each district.
- Integrate Celery for asynchronous updating of forecast data

## Technologies Used

- Django>=3.1.7
- djangorestframework>=3.12.4
- psycopg2-binary>=2.8.6
- openmeteo-requests>=1.2.0
- requests-cache>=1.2.0
- pandas>=2.0.0
- retry-requests>=2.0.0
- celery>=5.3.6
- django-celery-beat>=2.6.0
- Docker Compose
## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Seamul/Weather-Forecast-API.git
   cd Weather-Forecast-API

   ```

2. **Set Up Environment Variables:**
   - install Docker and Docker compose


3. **Build and Run the Docker Containers:**
   ```bash
   docker-compose up --build
   ```

4. **Run Database Migrations and Load Initial Districts Data:**
   ```bash
   docker-compose up
   ```


5. **Access the API:**
   Open your web browser and go to `http://0.0.0.0:8700/` to access the API endpoints.
   **Endpoint Description:**

   **POST /api/update_forecast_data/**
   
   **Purpose:**
   
   This endpoint triggers an update of forecast data. The process may take some time as it involves fetching and updating the forecast data. While ideally suited for automation, this functionality can also be initiated manually for simplicity.
   
   **Implementation Details:**
   
   To ensure timely updates, the endpoint is designed to integrate with Celery and Celery Beat. This allows for scheduled execution, ensuring that forecast data is updated regularly, ideally on a daily basis. However, for simplicity, manual invocation is also supported.
   
   **Usage:**
   
   - **Manual Invocation:** Send a POST request to the specified endpoint to trigger the update process manually.
     
     Example: `POST /api/update_forecast_data/`
     
   
   **Note:** The update process may take some time to complete, depending on various factors such as data availability and processing speed. Therefore, patience is advised during execution.
   
   **Recommendation:**
   
   For optimal performance and reliability, it is recommended to configure Celery and Celery Beat to handle automated updates. This ensures timely and consistent updates of forecast data without manual intervention.


  
## API Endpoints


- `POST /api/update_forcast_data/`: Trigger an update of forecast data. This endpoint is needed to trigger once a day to update forecast data and is not accessible to users directly.
- `GET /api/get_average_temperature/`: Get the average temperature across all districts.
- `POST /api/compare_temperature/`: Compare the temperature between two locations on a specified travel date.

### Example Request for Comparing Temperature
```http
POST http://0.0.0.0:8700/api/compare_temperature/
Content-Type: application/json

{
  "present_location": "Dhaka",
  "destination_location": "Gopalganj",
  "travel_date": "2024-03-26"
}
```

## Access Credentials

To access the system Admin

- **Username:** admin
- **Password:** admin_password



