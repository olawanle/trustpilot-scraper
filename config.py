"""
Configuration file for Trustpilot Email Scraper
"""

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Scraping Configuration
DEFAULT_MAX_COMPANIES = 10
DEFAULT_MAX_EMAILS_PER_COMPANY = 50
DEFAULT_DELAY_BETWEEN_REQUESTS = 2  # seconds
DEFAULT_PAGE_LOAD_TIMEOUT = 30  # seconds
DEFAULT_ELEMENT_TIMEOUT = 10  # seconds

# Chrome Driver Configuration
CHROME_HEADLESS = True
CHROME_WINDOW_SIZE = '1920,1080'
CHROME_DISABLE_GPU = True
CHROME_NO_SANDBOX = True
CHROME_DISABLE_DEV_SHM = True

# Trustpilot Configuration
TRUSTPILOT_BASE_URL = "https://www.trustpilot.com"
TRUSTPILOT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_DELAY = 2  # seconds between requests
RATE_LIMIT_MAX_REQUESTS_PER_MINUTE = 30

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Export Configuration
EXPORT_CSV_ENABLED = True
EXPORT_JSON_ENABLED = True
EXPORT_FILENAME_PREFIX = "trustpilot_emails"

# Security Configuration
CORS_ENABLED = True
CORS_ORIGINS = ['*']  # Configure appropriately for production

# Error Handling
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds
