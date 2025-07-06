# Database config

import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

base_config = {"host": "localhost", "user": db_user, "password": db_password}
database_name = "web_scraped_data"

try:
    # Connect to MySQL server
    conn = mysql.connector.connect(**base_config)
    cursor = conn.cursor()

    # Create the database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")