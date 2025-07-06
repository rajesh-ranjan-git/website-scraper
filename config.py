# Database config

import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    'host': 'localhost',
    'user': db_user,
    'password': db_password,
}

DB_CONFIG["database"] = "web_scraped_data"

try:
    # Connect to MySQL server
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create the database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG.database_name}")
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")