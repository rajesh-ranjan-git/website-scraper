import mysql.connector
import json

from config import base_config, database_name

# Insert data to database
def insert_data_to_db(source_url, text_content, image_urls, link_urls, tables_html):

    try:
        db_config = base_config.copy()
        db_config["database"] = database_name
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS web_scraped_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    source_url VARCHAR(2083),
                    text_content TEXT,
                    image_urls LONGTEXT,
                    link_urls LONGTEXT,
                    tables_html LONGTEXT
                )
            """
        )

        # Insert scrapped data
        cursor.execute(
            """
                INSERT INTO web_scraped_data (
                    source_url, text_content, image_urls, link_urls, tables_html) VALUES (%s, %s, %s, %s, %s
                )
            """,
            (
                source_url,
                text_content,
                json.dumps(image_urls),
                json.dumps(link_urls),
                json.dumps(tables_html),
            ),
        )

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ All data inserted with source URL : {source_url}.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")