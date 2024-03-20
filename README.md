

---

# Django API Docker Setup

This project provides a Dockerized environment for running a Django API along with a PostgreSQL database.

## Prerequisites

- Docker installed on your system.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Seamul/django-drf-fresh-project.git
   ```

2. Navigate to the project directory:

   ```bash
   cd django-drf-fresh-project
   ```

3. Build the Docker images:

   ```bash
   docker-compose build
   ```

4. Start the services:

   ```bash
   docker-compose up
   ```

   The Django API will be accessible at [http://localhost:8700](http://localhost:8700).

## Configuration

### PostgreSQL

- **Hostname:** `django_postgres`
- **Database Name:** `postgres`
- **Username:** `postgres`
- **Password:** `postgres`
- **Port:** `5432`

### Django API

- **Hostname:** `django_api`
- **Port:** `8700`

## Docker Compose Services

- **db:** PostgreSQL container.
- **api:** Django API container.

## Dockerfile

The Dockerfile sets up a Python environment, installs required dependencies, and copies the project files into the container.

## Requirement File

The `requirements.txt` file lists the Python packages required to run the Django API.

---

Feel free to customize this template to add any additional information specific to your project. Make sure to replace `<repository_url>` with the actual URL of your Git repository.

Let me know if you need any further assistance!
# Weather-Forecast-API
