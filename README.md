# Company_App

## Description
Company_App is a Django-based REST API connected to a PostgreSQL database. It allows users to manage companies they own. Each user can create, view, and update their companies, with restrictions such as a maximum of 5 companies per user and limited update fields. The API includes token-based authentication and Swagger documentation.

## Setup

### Environment Variables
To configure Company_App, follow these steps:
1. Duplicate the `example.env` file as `.env`.
2. Populate the `.env` file with your specific environment variable values. Default values will be used if not provided.

All database configuration settings are managed within the `.env` file.

## Running the App Locally

You can run Company_App in your local environment:

### 1. Running Directly in Local Environment

For local development outside Docker:

#### Steps:
1. Ensure Python 3.8+ is installed.
2. Create and activate a virtual environment.
3. Use the existing `.env` file with modified `DB_HOST` (`x.x.x.x` for remote database).
4. Install dependencies: `pip install -r requirements.txt`.
5. Configure the PostgreSQL database (creating a database and an user).
6. Run database migrations: `python3 manage.py makemigrations`, `python3 manage.py migrate`.
7. Create a superuser: `python3 manage.py createsuperuser`.
5. Start the app: `python3 manage.py runserver`.

## Swagger UI
Explore the API documentation via Swagger UI at `http://127.0.0.1:8000/swagger/`.

## Error Handling
Custom error handling ensures consistent error responses.

