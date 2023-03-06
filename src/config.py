# Index Scraper
INDEX_SCRAPER_CONFIG = {}

# Table Scraper
DEFAULT_BATCH_SIZE = 20

# URL
INDEX_URL = "https://www.sec.gov/Archives/edgar/daily-index/"
FILINGS_URL = "https://www.sec.gov/Archives/"

# HTTP
DEFAULT_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
DEFAULT_TIMEOUT = 5

# Database
DB_CONFIG = {
    'name': 'edgar_db',
    'user': 'sec_edgar_scrapper',
    'password': 'Pass123!',
    'host': 'localhost',
    'port': '5432',
}

# Table Manager
TABLE_MANAGER_CONFIG = {}
