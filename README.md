# 🕸️ Website Scraper with MySQL Storage

This Python-based web scraper is designed to extract data from a target website and store the scraped data in a MySQL database for further analysis or processing.

## 🚀 Features

- Scrapes structured data from a website using `requests`, `BeautifulSoup`.
- Saves extracted data to a MySQL database.
- Modular and extensible codebase.
- Handles errors gracefully and ensures data integrity.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Libraries:**
  - `requests` (for fetching web pages)
  - `beautifulsoup4` (for parsing HTML)
  - `mysql-connector-python` (for database interaction)
- **Database:** MySQL

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/website-scraper.git
cd website-scraper
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

```bash
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'your_database_name'
}
```

### 4. Run the Scraper

```bash
python scraper.py
```

## 📁 Project Structure

```bash
website-scraper/
│
├── config.py            # MySQL DB configuration
├── scraper.py           # Main script to scrape and store data
├── database.py          # DB connection and insert logic
├── utils.py             # (Optional) Utility functions
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🧪 Example Output

Scraped data will be inserted into a table like:

```bash
CREATE TABLE IF NOT EXISTS web_scraped_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source_url VARCHAR(2083),
  text_content TEXT,
  image_urls LONGTEXT,
  link_urls LONGTEXT,
  tables_html LONGTEXT
)
```

## ✅ Best Practices

- Avoid scraping sites without permission. Always check the site’s robots.txt.
- Respect rate limits by adding sleep() between requests.
- Implement retry logic for robustness.
- Sanitize and validate all scraped data before storing.

## 👨‍💻 Author

### Rajesh Ranjan

[GitHub](https://github.com/rajesh-ranjan-git/website-scraper) | [LinkedIn](https://www.linkedin.com/in/rajesh-ranjan-660b1b13a/)

- Email: rajeshranjan8271.com
- Contact Number: 9999340771

<hr />

We hope you enjoy using Website Scraper!
