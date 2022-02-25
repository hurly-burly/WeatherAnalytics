# WeatherAnalytics

Analysis of historical weather data.

## Description

The application calls OpenWeather API to fetch historical data for last 5 days for 10 different locations whose latitude and longitude are given.

## Table of contents

1. Technologies and Frameworks
2. Installation and Run
3. How to run in Docker
4. Author
5. Contributing
6. License

## Technologies and Frameworks

The project is created with:
* Python 3.6
* Docker 20.10.0
* SQLite

## Installation and Run

The application can be run run directly as python script. 
Python 3.6 or higher version must be installed in the local system.

```bash
$ pip install -r requirements.txt

$ python app.py
```

The application can also be run in docker container.
```
$ docker-compose up
```

## How to run in Docker

1. Clone the project from Github.
```
git clone <repository-url>
```

2. Move to project directory 'WeatherAnalytics'.

3. Set API Key in the variable API_KEY in 'config.py' file. \
     API_KEY=""

4. Run below command to build image and run the app in container.
```
$ docker-compose up
```

5. The app will run and store data in SQLite Database 'weather.db' that will get created inside 'SQLiteDB' directory in project directory.

6. Extracts of data from this Database tables will also be generated as csv files inside 'SQLiteDB' directory.

7. Application logs (files with extension .log) will be generated inside 'logs' directory in project directory.

8. For fetching data for a different location\city, update or add Name, Latitude and Longitude of the location in LAT_LONG variable (python dict).

9. For changing to a different unit for Temperature, update value in TEMP_UNIT variable, currently set as 'metric' for getting temperature in Celsius.

10. After done with the changes, to rebuild the image and run the app, use the below command.
```
$ docker-compose up --build
```

## Author 


## Contributing


## License

