import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")

    # Switch DB automatically if pytest is running
    if "pytest" in sys.modules:
        DB_NAME = os.getenv("TEST_DB_NAME", "mydb_test")
    else:
        DB_NAME = os.getenv("DB_NAME", "mydb")

    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = os.getenv("APP_PORT", "8000")

settings = Settings()
