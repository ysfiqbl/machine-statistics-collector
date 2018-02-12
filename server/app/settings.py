import os

# Celery.
CELERY_BROKER_URL = 'amqp://admin:rabbitmq@rabbitmq:5672'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5


# Application variables
APP_HOME = 'app'
CLIENT_SCRIPT_NAME = 'remote_script.py'
CLIENT_CONFIG_FILE = 'config.xml'


# Database Configuration
DB_URI = 'mysql://root:root!123@db:3306/mstats?host=db?port=3306?password=root!123'
DB_URI_TEST = 'mysql://root:root!123@db:3306/mstats_test?host=db?port=3306?password=root!123'
DB_TEST_ON = False
DB_DEBUG_ON = False

# Mail Settings
MAIL_DEFAULT_SENDER = 'noreply@mstats.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'crossover.app.test@gmail.com'
MAIL_PASSWORD = 'Cr0s5Ov3r!123'

MAIL_TO_SEND = 1
MAIL_SENDING = 2
MAIL_SENT = 3
MAIL_FAILED = 4

# Derived variables
CLIENT_CONFIG_FILE_PATH = os.path.join(APP_HOME, CLIENT_CONFIG_FILE)
CLIENT_SCRIPT_FILE_PATH = os.path.join(APP_HOME, CLIENT_SCRIPT_NAME)
CLIENT_COMPILED_SCRIPT_NAME = '{0}c'.format(CLIENT_SCRIPT_NAME)
CLIENT_COMPILED_SCRIPT_FILE_PATH = os.path.join(APP_HOME, CLIENT_COMPILED_SCRIPT_NAME)


