import requests
from bs4 import BeautifulSoup
import extruct
from w3lib.html import get_base_url
from dateutil import parser


# Helper Function
def clean_text(text):
    return " ".join(text.strip().split())


# Extract all links URLs
def get_link_urls(soup):
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

    print("\n=== Getting Story Link URLs ===")
    return updated_urls


# Extract all story links URLs
def get_story_link_urls(source_url, headers):
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


# Get Date Modified
def get_date_modified(url, headers):
    response = requests.get(url, headers=headers)
    base_url = get_base_url(response.text, response.url)
    data = extruct.extract(response.text, base_url=base_url)

    for item in data.get("json-ld", []):
        if "dateModified" in item:
            try:
                dt = parser.parse(item["dateModified"])
                return dt.replace(tzinfo=None)
            except Exception as e:
                print(
                    f"⚠️ Failed to parse dateModified: {item} - {item['dateModified']} — {e} for URL : {url}"
                )
                return None
    return None


# Get parent div
def get_parent_div(source_url, headers):
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
