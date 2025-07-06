import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import logging

# Load API key from .env file
load_dotenv()
openai_api_key = os.getenv("GITHUB_OPENAI_API_KEY")

# Initialize OpenAI client
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"

client = OpenAI(
    base_url=endpoint,
    api_key=openai_api_key,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Define the URL and headers
url = "https://cleartax.in/s/gst-rates-revised"
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# Step 2: Request the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

# Step 3: Find the parent div of the <h1> tag
h1_tag = soup.find('h1')
if not h1_tag:
    raise Exception("No <h1> tag found")

parent_div = h1_tag.find_parent()

# Step 4: Extract all text under this parent div
text_content = parent_div.get_text(separator="\n", strip=True)

# Step 5: Extract all tables as raw HTML
tables_html = [str(table) for table in parent_div.find_all('table')]

# Step 6: Extract all image URLs
images = parent_div.find_all('img')
image_urls = [img['src'] for img in images if img.get('src')]

# Step 6: Extract all links URLs
links = parent_div.find_all('a')
link_urls = [a['href'] for a in links if a.get('href') and a['href'].startswith('http')]

# Step 7: Print results
print("=== TEXT CONTENT (first 1000 characters) ===")
print(text_content[:1000] + '...')
print(text_content)

print("\n=== IMAGE URLs ===")
for url in image_urls:
    print(url)

print("\n=== Link URLs ===")
for url in link_urls:
    print(url)

print("\n=== RAW <table> HTML ===")
for idx, table_html in enumerate(tables_html, 1):
    print(f"\n--- Table {idx} ---\n")
    print(table_html)

# def get_summary(text):
#     logger.info("Generating summary...")
#     try:
#         response = client.chat.completions.create(
#             messages = [
#                 {
#                     "role": "system",
#                     "content": "You are an assistant that analyze the contents scraped from a website and summarizes it to a meaningful story.",
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""Please generate a summary of the following data scraped from a site for a meaningful story :{text}
#                     Return the result in paragraph type and if there are any statistic data, keep it as it is in the response. If the data appears to be of a list, keep the list intact.""",
#                 }
#             ],
#             temperature=0.7,
#             top_p=1,
#             model=model
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         logger.error(f"Error during summarization: {e}")
#         return "Error generating summary."
    
# summary = get_summary(text_content)
# print(f"Summary : {summary}")
