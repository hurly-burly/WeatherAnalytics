import calendar
import datetime
import logging
import os
import requests
import time
import uuid
import pandas as pd
import sqlite3 as sql

from config import API_KEY, BASE_DIR, REPLICATED_LOG_DIR_PATH, DB_NAME, RAW_DATA_TABLE, DATASET1, DATASET2, \
    REPLICATED_DB_DIR_PATH
from constants import LAT_LONG, MAX_RETRIES, TEMP_UNIT, DROP_DATASET1_TABLE_QUERY, CREATE_DATASET1_QUERY, \
    DROP_DATASET2_TABLE_QUERY, CREATE_DATASET2_QUERY

# container path
LOG_DIR_PATH = os.path.join(BASE_DIR, 'logs')
DB_DIR_PATH = os.path.join(BASE_DIR, 'sqlitedb')


def extract_db_data(conn, log, tables):
    """write db records as excel"""
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_csv(f'{DB_DIR_PATH}/{table}.csv', index=False)
        log.info(f"DB table '{table}' extract generated at {DB_DIR_PATH}/{table}.csv")


if __name__ == "__main__":

    print("Process started")

    try:
        run_id = uuid.uuid4().int  # unique id for each app log file
        # configure a logger
        LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, filename=f'{LOG_DIR_PATH}/{run_id}.log', filemode='w',
                            format=LOG_FORMAT)
        # create a logger
        logger = logging.getLogger()
        print(f"log file availaible at: {REPLICATED_LOG_DIR_PATH}/{run_id}.log", )
        logger.info("------------Execution started--------------")

        # check if API_KEY is set
        if not API_KEY:
            logger.error("API key not found: set a valid API key value to API_KEY variable in config.py")
            raise Exception("API_KEY not found")

        BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"

        print("sending requests to OpenWeather API ...")
        logger.info("sending requests to OpenWeather API ...")
        weather_data_list = []
        for location, lat_long in LAT_LONG.items():
            for nday in range(0, 5):
                date = datetime.datetime.utcnow() - datetime.timedelta(nday)
                utc_time = calendar.timegm(date.utctimetuple())
                DATE_TIMESTAMP = utc_time  # Date from the previous five days (Unix time, UTC time zone)
                # full URL
                URL = f"{BASE_URL}lat={lat_long[0]}&lon={lat_long[1]}&units={TEMP_UNIT}&dt={DATE_TIMESTAMP}&appid={API_KEY}"
                retries = 0
                response = None
                while True:
                    # HTTP request
                    response = requests.get(URL)
                    # checking the status code of the request
                    if response.status_code != 200 and retries < MAX_RETRIES:
                        retries += 1
                        time.sleep(1)  # sleep for one second before retrying
                        logger.info(f"Retrying... {retries}")
                        continue
                    break
                logger.info(f"HTTP Response Status Code {response.status_code}")
                if response.status_code == 200:
                    # getting data in the json format
                    data = response.json()  # getting the data
                    latitude = data['lat']
                    longitude = data['lon']
                    main = data['hourly']
                    for i in range(len(main)):
                        date = main[i]['dt']
                        temperature = main[i]['temp']
                        weather_data_list.append([location, latitude, longitude,
                                                  datetime.datetime.utcfromtimestamp(int(date)).strftime(
                                                      '%Y-%m-%d %H:%M:%S'),
                                                  temperature])
                else:
                    data = response.json()  # API returning json even if the request is unsuccessful
                    error_msg = ''
                    if data:
                        error_msg = data['message']
                    logger.error(f"Error in the HTTP request - {response.status_code}: {error_msg}")

        weather_df = pd.DataFrame(weather_data_list,
                                  columns=["Location", "Latitude", "Longitude", "Date_time", "Temperature"])
        weather_df.drop_duplicates(subset=None, keep='first', inplace=True)

        print("Saving data to DB...")

        try:
            # DB operations
            connection = sql.connect(f"{DB_DIR_PATH}/{DB_NAME}.db")  # sqlite connection object
            logger.info(f"Connection established with '{DB_NAME}' database")
            # saving dataframe to DB
            weather_df.to_sql(RAW_DATA_TABLE, connection, if_exists='replace')
            logger.info(f"response data Saved to DB table '{RAW_DATA_TABLE}'")
            cursor = connection.cursor()
            cursor.execute(DROP_DATASET1_TABLE_QUERY)
            logger.info(f"table '{DATASET1}', if exists, dropped")
            cursor.execute(CREATE_DATASET1_QUERY)
            logger.info(f"table '{DATASET1}' created")
            cursor.execute(DROP_DATASET2_TABLE_QUERY)
            logger.info(f"table '{DATASET2}', if exists, dropped")
            cursor.execute(CREATE_DATASET2_QUERY)
            logger.info(f"table '{DATASET2}' created")
            connection.commit()
            logger.info(f"SQLite DB available at: {DB_DIR_PATH}/{DB_NAME}.db")
            print(f"SQLite DB available at: {REPLICATED_DB_DIR_PATH}/{DB_NAME}.db")
            extract_db_data(connection, logger,
                            [f'{RAW_DATA_TABLE}', f'{DATASET1}', f'{DATASET2}'])  # extract data from DB tables
            print(f"DB tables extracts available in {REPLICATED_DB_DIR_PATH}/")
            connection.close()
        except Exception as e:
            logger.error("Database Error : ", str(e))
            raise Exception("Database Error : ", str(e))

    except Exception as e:
        print(str(e))
    else:
        logger.info("------------Execution successful--------------")
    finally:
        print("Process stopped")
