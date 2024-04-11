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
1. [IF NEEDED] Set environment variables to tell Flask to run in development mode (enables features like debugger and auto-reloader)
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


---

## Deployment

Instructions on how to deploy the application on a live system, such as Heroku:

### Heroku Setup

1. **Install the Heroku CLI**: Ensure you have the Heroku Command Line Interface (CLI) installed on your system. You can download it from [Heroku's website](https://devcenter.heroku.com/articles/heroku-cli).

2. **Login to Heroku**: Open your terminal and log in to Heroku using the command `heroku login`. This opens your web browser to log in to your Heroku account.

### Create a Heroku App

- Execute `heroku create` to create a new app on Heroku. This command outputs the web URL for your application and a Git URL. Note down the web URL, as you'll need it to access your deployed application.

### Set Up Environment Variables

- Set any necessary environment variables on Heroku using the command `heroku config:set VAR_NAME=value`. For each environment variable required by your application, repeat this command with the appropriate `VAR_NAME` and `value`. For example:

```bash
heroku config:set REACT_APP_API_URL=https://your-api-url.com
```

### Configure Buildpacks

- Depending on your application's stack, you may need to specify one or more buildpacks. Heroku uses buildpacks to determine how to build and run your application.
  - For a **Node.js** application, set the Node.js buildpack:
```bash
heroku buildpacks:set heroku/nodejs
```
  - For applications that require **multiple languages** (e.g., a React frontend and a Python Flask backend), add buildpacks in the order they should be executed:
```bash
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
```

### Deploy Your Application

- **Deploy your application** by pushing your code to the Heroku remote. If your main branch is named `main`, use:
```bash
git push heroku main
```

Replace main with the name of your branch if using a different branch name.  
- Monitor the deployment process by viewing the logs with:
```bash
heroku logs --tail
```

### Access Your Deployed Application
- Once deployed, access your application through the web URL provided by Heroku. You can also open your app directly from the CLI with:
```bash
heroku open
```

### Additional Considerations
- Database Setup: If your application uses a database, make sure to provision and configure the appropriate add-on in Heroku.

- Custom Domain: Configure a custom domain via the Heroku dashboard or CLI if required.

- Performance and Scaling: Monitor your application's performance. Scale dynos as needed to handle the load efficiently.