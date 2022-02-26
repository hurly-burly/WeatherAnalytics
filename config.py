"""definition for project parameters"""

API_KEY = ""  # secret private API
DB_NAME = "weather"
RAW_DATA_TABLE = 'RAW'
DATASET1 = 'DATASET1'
DATASET2 = 'DATASET2'

BASE_DIR = '/var/lib'  # path in container instance

# local paths for logs and DB replication
REPLICATED_LOG_DIR_PATH = 'logs'
REPLICATED_DB_DIR_PATH = 'SQLiteDB'
