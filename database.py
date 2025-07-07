import mysql.connector
import json

from config import DB_CONFIG
from utils import (
    get_parent_div,
    get_text_content,
    get_image_urls,
    get_links_in_story,
    get_tables_html,
    get_date_modified,
)


# Insert data to database
def insert_data_to_db(source_url, headers):
    try:
        db_config = DB_CONFIG.copy()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS web_scraped_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    source_url VARCHAR(767) UNIQUE,
                    date_modified DATETIME,
                    text_content TEXT,
                    image_urls LONGTEXT,
                    link_urls LONGTEXT,
                    tables_html LONGTEXT
                )
            """
        )

        # Check if source_url already exists
        cursor.execute(
            "SELECT date_modified FROM web_scraped_data WHERE source_url = %s",
            (source_url,),
        )
        existing_record = cursor.fetchone()

        if existing_record:
            existing_date_modified = existing_record[0]

            date_modified = get_date_modified(source_url, headers)
            if existing_date_modified == date_modified:
                print(
                    f"⚠️ Skipping: No update needed for URL: {source_url} (dateModified unchanged)"
                )
            else:
                # Get parent div to update record
                parent_div = get_parent_div(source_url, headers)
                if parent_div == None:
                    cursor.close()
                    conn.close()
                    print(f"No record to update for URL: {source_url}")
                    return None

                # Update the record
                cursor.execute(
                    """
                        UPDATE web_scraped_data
                        SET date_modified = %s,
                            text_content = %s,
                            image_urls = %s,
                            link_urls = %s,
                            tables_html = %s
                        WHERE source_url = %s
                    """,
                    (
                        date_modified,
                        get_text_content(parent_div),
                        json.dumps(get_image_urls(parent_div)),
                        json.dumps(get_links_in_story(parent_div)),
                        json.dumps(get_tables_html(parent_div)),
                        source_url,
                    ),
                )
                conn.commit()
                print(f"🔁 Updated existing record for URL: {source_url}")
        else:
            # Insert new record
            cursor.execute(
                """
                    INSERT INTO web_scraped_data (
                        source_url, date_modified, text_content, image_urls, link_urls, tables_html
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    source_url,
                    date_modified,
                    get_text_content(parent_div),
                    json.dumps(get_image_urls(parent_div)),
                    json.dumps(get_links_in_story(parent_div)),
                    json.dumps(get_tables_html(parent_div)),
                ),
            )

            # Commit changes and close connection
            conn.commit()
            print(f"✅ Inserted new record for URL: {source_url}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
