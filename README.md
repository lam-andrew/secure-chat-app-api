# secure-chat-app-api
API for fullstack secure chat application

# Flask Backend for Secure Chat Application
This is the Flask backend for a secure chat application, responsible for handling user authentication, WebSocket connections for real-time messaging, and interaction with the database. It provides RESTful APIs that the React frontend consumes.

## Getting Started
These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
Python 3.6 or newer
pip for installing dependencies
Virtual environment (recommended) `python -m venv venv`

## Setup
1. Clone the Repository

If you haven't already, clone the repository to your local machine.
```
Copy code
git clone https://github.com/your-username/secure-chat-application.git
cd secure-chat-application/backend
```
2. Create a Virtual Environment

To create a virtual environment, run the following command in the backend directory:
```python -m venv venv```
Activate the virtual environment:
- On macOS/Linux:
```source venv/bin/activate```
- On Windows:
```venv\Scripts\activate```

3. Install Dependencies

With the virtual environment activated, install the project dependencies using pip:
```pip install -r requirements.txt```

### Update requirements.txt file
Activate Virtual Environment and run:
`pip freeze > requirements.txt` 


## Configuration
**Environment Variables:** Configure necessary environment variables for your project, such as database URLs, OAuth credentials, and other sensitive settings. Create a .env file in the root of the `backend` directory and populate it with the required variables.

#### Running the Application
To run the application on your local development machine:
1. Set environment variables to tell Flask to run in development mode (enables features like debugger and auto-reloader)
```
export FLASK_APP=app.py
export FLASK_ENV=development
```
2. Run the Flask app
```flask run``` or ```python app.py```


## Structure
- app.py: The entry point to the Flask application.
- /api: Directory for your application's route definitions.
- /models: Contains ORM models.
- /services: Business logic of your application.
- /utils: Utility functions and helpers.
- requirements.txt: A list of project dependencies.


## Deployment
Instructions on how to deploy the application on a live system, such as Heroku:

1. Heroku Setup: Ensure you have the Heroku CLI installed and are logged in.
2. Create a Heroku App: `heroku create`
3. Set Environment Variables on Heroku: Use `heroku config:set VAR_NAME=value` for each environment variable.
4. Deploy: Push your code to Heroku using `git push heroku main`.