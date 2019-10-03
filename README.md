# My Personal Website Back End

This is my personal website back end RESTful API service built with `Flask` library. This RESTful API is used for authentication, data and many other cool endpoints. The[edwardnunez.io-web](https://github.com/dotRollen/edwardnunez.io-web) repo is where the web interface is hosted and consumes this RESTful API. If you need access to the live RESTful API please feel free to contact me for temporary access!


## Local Setup
### Requirements
The application was built with the following environment dependencies.

| Software        | Version           | Link  |
| ------------- |:-------------:| -----:|
| Python | ^3.7.0 | [Documentation](https://docs.python.org/3/) |

### Deploying

#### Initial Local Setup

It's recommended that the application be installed in a virtual environment. When Python ^3.7 is installed, use CMD/Terminal to create a virtual environment with the following command.

> For Windows
Create the environment
`python -m venv env` 

Activate the environment
`env\Scripts\activate`

> For Mac
Create the environment
`python3 -m venv env`

Activate the environment
`source env/bin/activate`

> Both systems
Deactivate the environment
`deactivate`

> Please note that the app requires a MongoDB server locally or a URI to be defined in the environment variable.

##### Required Environment Variables

```
MAIL_SERVER="MAIL SERVER URL"
MAIL_PORT=INTEGER
MAIL_USE_TLS=BOOLEAN
MAIL_USERNAME="EMAIL@EMAIL.COM"
MAIL_PASSWORD="PASSWORD"

BACKEND_ADMIN="YOUREMAIL@EMAIL.COM"
BACKEND_ADMIN_PASSWORD="PASSWORD"
BACKEND_ADMIN_USERNAME="USERNAME"
FLASK_DEBUG=" 1 || 0 "
FLASK_CONFIG="development || production"
```

##### Optional Environment Variables

> For development host DB setup
```
DEV_MONGODB_HOST='hostname' || default is "localhost"
DEV_MONGODB_DATABASE='databaseName' || default is 'BackendDev'
DEV_MONGODB_USER='username' || default is None
DEV_MONGODB_PASSWORD='password' || default is None
DEV_MONGODB_PORT='port' || default is 27017
```

> For production DB setup
```
MONGODB_URI= 'uri' || default is None
```

#### Install Dependencies & Run Locally

We're going to install the development environment dependencies to the virtual environment and then set the environment variable for FLASK_APP to the source code package. We will the deploy the initial setup of the app (admin, roles and so on). After that use the last command to run the server.

> For Mac
1. `pip install requirements/dev.txt`
2. `export FLASK_APP=backend.manage`
3. `flask deploy`
4. `flask run`

> For Windows
1. `pip install requirements\dev.txt`
2. `set FLASK_APP=backend.manage`
3. `flask deploy`
4. `flask run`
