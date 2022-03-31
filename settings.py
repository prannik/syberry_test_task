import os
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#Database
DATABASE = {
    "drivername": "mysql+pymysql",
    "host": env('DATABASE_HOST'),
    "username": env('DATABASE_USER'),
    "password": env('DATABASE_PASSWORD'),
    "database": env('DATABASE_NAME'),
}
