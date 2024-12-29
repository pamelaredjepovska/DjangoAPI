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

You can run Company_App in your local environment in two ways:

### 1. Running Directly in Local Environment

For local development outside Docker:

#### Steps:
1. Ensure Python 3.8+ is installed.
2. Create and activate a virtual environment.
3. Use the existing `.env` file with modified `DB_HOST` (`localhost`, `x.x.x.x` for remote database).
4. Install dependencies: `pip install -r requirements.txt`.
5. Configure the PostgreSQL database (creating a database and an user).
6. Run database migrations: `python3 manage.py makemigrations`, `python3 manage.py migrate`.
7. Create a superuser: `python3 manage.py createsuperuser`.
8. Start the app: `python3 manage.py runserver`.
9. Access the app at `http://127.0.0.1:8000/`.

### 2. Using Docker Container

Running Company_App in a Docker container is the recommended approach, aligning with production deployment standards:

#### Setup Steps:
1. Set `DB_HOST=docker-djangodb` in the `.env` file.
2. Define `TEST_HOST=0.0.0.0` and choose `TEST_PORT=8000` for the app's listening port.
3. Launch the Django app in debug mode:
   - Execute `docker compose up --build`.
   - For rebuilding images and removing orphaned containers: `docker compose up --build --remove-orphans`.
   - Docker will build two images and start containers named `docker-djangodb` (Postgres instance) and `docker-djangoapi` (the app) respectively.
   - Access the app at `TEST_HOST:TEST_PORT`.

#### Container Manipulation:
- The Postgres database initializes with default data (refer to the [sql](sql) folder).
- Persistent database data is stored in `postgres_data` (new data persists across app restarts).
- To reset the database, delete `postgres_data`: `sudo rm -rf postgres_data` and rerun `docker compose up --build`.
- Inspect the `docker-djangodb` container: `docker exec -it docker-djangodb psql -d <db_name> -U <db_user>`.

## Testing Email Functionality with MailTrap
Use MailTrap to test email functionality safely during development. 
Here's how:
1. Sign Up: Create an account on MailTrap and log in.
2. Create Inbox: Add a new inbox in the dashboard.
3. Get Credentials: Copy the SMTP settings (Host, Port, Username, Password) from your inbox.
4. Configure: Update your .env file:
    ```EMAIL_HOST=smtp.mailtrap.io
    EMAIL_PORT=your_mailtrap_port
    EMAIL_HOST_USER=your_mailtrap_username
    EMAIL_HOST_PASSWORD=your_mailtrap_password
    EMAIL_USE_TLS=True```
5.  Test Emails: Trigger email functionality and check the inbox for results.

**_Note_**: Use MailTrap only for development and testing, not in production.

## Swagger UI
Explore the API documentation via Swagger UI at `http://127.0.0.1:8000/swagger/`.

## Error Handling
Custom error handling ensures consistent error responses.

