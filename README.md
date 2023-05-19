# Software engineering Weather API Project

This is a weather API using OpenWeatherMap to fetch weather data for specific location.
To run the app, follow the steps below:

## How to use this API

Clone the repository at first:

```
  git clone https://github.com/Ismar1509/Weather-API-Python.git
```
After you have cloned the repository, you must ensure to install python if it is already not installed.

Install Python: The first step is to install Python, which is required to run Django and this project. You can download the latest version of Python from the official Python website and follow the installation instructions for your operating system.
```
  https://www.python.org
```
Set up a virtual environment (optional but recommended): It's a good practice to create a virtual environment to isolate project dependencies. You can create a virtual environment using the venv module that comes bundled with Python. In the project's root directory, you can run the following command to create a virtual environment:

```
  python -m venv myenv
```
This will create a new virtual environment named myenv.

For Linux, command below is used instead

```
  python3 -m venv myenv
```
If on Linux you cannot create venv, you should install python3-venv

```
  apt install python3.10-venv
```

Activate the virtual environment - After creating the virtual environment, you need to activate it. The process varies depending on the operating system:

Windows
```
  myenv\Scripts\activate.bat
```

MacOS or Linux
```
  source myenv/bin/activate
```

Navigate to this project and use command

```
  pip install -r requirements.txt
```

Once the virtual environment is activated, you can install the project dependencies specified in project's requirements.txt file. You can use the command above to install the dependencies. It will install all the required packages and libraries for the project.

Place API key into API_KEY.py 
**API KEY HAS BEEN PROVIDED TO THE PROFESSOR ON TEAMS ASSIGNMENT**

If your IDE suggests that there are migrations to be done, use the following command:

```
  python manage.py migrate
```
Run the development server: Finally, you can start the development server to run this Django project. You can use the following command after navigating to src:

```
  python manage.py runserver
```
This will start the development server, and you can access the project by visiting http://localhost:8000 in your web browse

Before starting the server, use command 

```
  python manage.py createsuperuser
```
By using this command, you will be asked to enter username, email and password twice.
This will store your super user in database and it will be used for authentication.
To fill headers needed for authentication, use online bas64 generators to convert your username and password into bas64

Each time you want to fetch data using swagger and GET or POST request you will need to fill authorization header
Fill it like this:

Basic <base64username:password>
e.g. your username is admin123 and password is softeng123


```
  Basic YWRtaW4xMjM6c29mdGVuZzEyMw==
```
This is described better in config.txt file

## Make API Requests
There are three API endpoints - current, forecast and history weather. They differ in their responses but also in data needed to make requests. All of them use location parameter, forecast uses additionally number of days between 1 and 7 for forecasting. Historical data needs beside location, start and end date (**start_date**, **end_date**) in format - **YYYY-MM-DD** 

And all of them are called using **POST** requests which is protected with basic authentication.
**GET** request is also available and has same basic authentication.
Recommended way of testing if Api fetches the data is through swagger that is also included

For Basic authentication, user needs keyword **Basic** and password converted to base64. Explanation of this is found in file config.txt

## Logging
API logs requests and logs can be found in the api_logs.log file

## Swagger
Swagger documentation can be accessed by going to the browser while the server is running and going to 
```
  http://localhost:8000/api/swagger/
```

## Postman collection
Postman collection is included inside of the project as .json file.
Testing through Postman is explained in config.txt file

