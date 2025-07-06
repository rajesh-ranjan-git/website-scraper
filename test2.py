import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import re
import os

def clean_text(text):
    return ' '.join(text.strip().split())

def extract_elements_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    elements_data = []

    last_heading = ""

    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'table']):
        if tag.name.startswith('h'):
            last_heading = clean_text(tag.get_text())
            elements_data.append({'Element': tag.name, 'Content': last_heading})

        elif tag.name in ['p', 'li']:
            text = clean_text(tag.get_text())
            if text:
                elements_data.append({'Element': tag.name, 'Content': text})

        elif tag.name == 'table':
            table_html = str(tag)

            # Find caption if present
            caption = tag.find('caption')
            table_title = clean_text(caption.get_text()) if caption else last_heading or "Unnamed Table"

            elements_data.append({
                'Element': f"table: {table_title}",
                'Content': table_html
            })

    return elements_data

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def scrape_and_save_individual_files(urls, output_dir='outputs'):
    if isinstance(urls, str):
        urls = [urls]

    os.makedirs(output_dir, exist_ok=True)

    for url in urls:
        print(f"Processing {url}")
        data = extract_elements_from_url(url)

        if data:
            df = pd.DataFrame(data)
            domain = urlparse(url).netloc.replace("www.", "")
            filename = sanitize_filename(domain) + ".csv"
            full_path = os.path.join(output_dir, filename)

            df.to_csv(full_path, index=False, encoding='utf-8-sig')
            print(f"Saved: {full_path}")
        else:
            print(f"No data extracted from {url}")

# Example usage:
if __name__ == "__main__":
    urls = [
        "https://example.com",
        # Add more URLs here
    ]
    scrape_and_save_individual_files(urls)
