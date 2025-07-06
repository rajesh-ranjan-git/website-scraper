import requests
from bs4 import BeautifulSoup
import mysql.connector
import json

# Define the URL and headers
source_url = "https://docs.cleartax.in/cleartax-learn/gst-rates-and-hsn-codes/gst-rates"
headers = {"User-Agent": "Mozilla/5.0"}

# Helper Function
def clean_text(text):
    return " ".join(text.strip().split())

# Request the page for parent div
response = requests.get(source_url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Extract all links URLs
def get_link_urls():
    links = soup.find_all("a")
    link_urls = [
        a["href"]
        for a in links
        if a.get("href")
        and (
            a["href"].lower().startswith("https://docs.cleartax.in/cleartax-learn")
            or "/cleartax-learn" in a["href"].lower()
        )
    ]

    updated_urls = list(
        map(
            lambda url: (
                f"https://docs.cleartax.in{url}"
                if url.startswith("/cleartax-learn")
                else url
            ),
            link_urls,
        )
    )
    print("\n=== Link URLs ===")
    for url in updated_urls:
        print(url)

    return updated_urls

# Extract all story links URLs
def get_story_link_urls(source_url):
    story_url_response = requests.get(source_url, headers=headers)
    story_soup = BeautifulSoup(story_url_response.text, "lxml")
    story_links = story_soup.find_all("a")
    story_link_urls = [
        a["href"]
        for a in story_links
        if a.get("href")
        and (
            a["href"].lower().startswith("https://cleartax.in/s/")
            or a["href"].lower().startswith("http://cleartax.in/s/")
        )
    ]

    return story_link_urls

# Extract all links in URL
def get_links_in_story(parent_div):
    links_in_story = parent_div.find_all("a")
    link_urls_in_story = [
        a["href"]
        for a in links_in_story
        if a.get("href")
        and (
            a["href"].lower().startswith("https://cleartax.in/s/")
            or a["href"].lower().startswith("http://cleartax.in/s/")
        )
    ]

    return link_urls_in_story

def get_parent_div(source_url):
    response = requests.get(source_url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # Find the parent div of the <h1> tag
    h1_tag = soup.find("h1")
    if not h1_tag:
        print(f"No <h1> tag found for {source_url}")
        return None

    parent_div = h1_tag.find_parent()
    return parent_div

# Extract all text under this parent div
def get_text_content(parent_div):
    text_content = []
    for tag in parent_div.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        if tag.name.startswith("h"):
            text_content.append(clean_text(tag.get_text(separator="\n", strip=True)))

        elif tag.name in ["p"]:
            text_content.append(clean_text(tag.get_text(separator="\n", strip=True)))

    final_text_content = "\n".join(text_content)
    return final_text_content

# Extract all image URLs
def get_image_urls(parent_div):
    images = parent_div.find_all("img")
    image_urls = [img["src"] for img in images if img.get("src")]
    return image_urls

# Extract all tables as raw HTML
def get_tables_html(parent_div):
    tables_html = [str(table) for table in parent_div.find_all("table")]
    return tables_html

# Insert data to database
def insert_data_to_db(source_url, text_content, image_urls, link_urls, tables_html):
    base_config = {"host": "localhost", "user": "root", "password": "root"}
    database_name = "web_scraped_data"

    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**base_config)
        cursor = conn.cursor()

        # Create the database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.close()
        conn.close()

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

story_link_urls = []
for url in get_link_urls():
    story_link_urls.extend(get_story_link_urls(url))

for url in list(set(story_link_urls)):
    parent_div = get_parent_div(url)
    if(parent_div == None):
        continue
    insert_data_to_db(
        url,
        get_text_content(parent_div),
        get_image_urls(parent_div),
        get_links_in_story(parent_div),
        get_tables_html(parent_div),
    )

print("✅ All data inserted to database.")