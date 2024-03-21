

---

# Weather-Forecast-API


This Django project serves as an API for managing district information in Bangladesh, including weather forecast data.

## Introduction

This API provides endpoints to retrieve information about districts in Bangladesh, including their names, coordinates, and weather forecasts. It includes functionality to update forecast data periodically using Celery tasks, but for simplicity, we'll run it manually.

## Features

- Retrieve a list of all districts.
- Retrieve detailed information about a specific district.
- Access weather forecast data for each district.
- Update forecast data periodically using Celery tasks (not implemented in this simple setup).

## Technologies Used

- Django>=3.1.7
- djangorestframework>=3.12.4
- psycopg2-binary>=2.8.6
- openmeteo-requests>=1.2.0
- requests-cache>=1.2.0
- pandas
- retry-requests>=2.0.0
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

4. **Run Database Migrations:**
   ```bash
   docker-compose up
   ```

5. **Load Initial Data:**
   ```bash
   docker-compose up initial_data.json
   ```

6. **Update Forecast Data (Optional):**
   Before accessing other API endpoints, you need to update the forecast data in your local DB using endpoint
   ```bash
   GET http://127.0.0.1:8000//api/update_forcast_data/
   ```

7. **Access the API:**
   Open your web browser and go to `http://127.0.0.1:8000/` to access the API endpoints.

## API Endpoints


- `GET /api/update_forcast_data/`: Trigger an update of forecast data.
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



