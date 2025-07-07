import requests
import extruct
from w3lib.html import get_base_url
from dateutil import parser


def get_date_modified(url):
    headers = {"User-Agent": "Mozilla/5.0"}
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


# Example usage
url = "https://cleartax.in/s/transitional-provisions-in-certain-cases-under-gst"
date_modified = get_date_modified(url)
print("Date Modified:", date_modified)
