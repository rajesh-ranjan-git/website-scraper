import requests
from bs4 import BeautifulSoup

from database import insert_data_to_db
from utils import (
    get_link_urls,
    get_story_link_urls,
)


# Define the URL and headers
source_url = "https://docs.cleartax.in/cleartax-learn/gst-rates-and-hsn-codes/gst-rates"
headers = {"User-Agent": "Mozilla/5.0"}

# Request the page for parent div
response = requests.get(source_url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

story_link_urls = []
for url in get_link_urls(soup):
    story_link_urls.extend(get_story_link_urls(url, headers))

for url in list(set(story_link_urls)):
    insert_data_to_db(
        url,
        headers,
    )

print("✅ All data inserted to database.")
