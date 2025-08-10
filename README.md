# Trustpilot Email Scraper

A fast and efficient web scraper for extracting company email addresses from Trustpilot.

## Features

- 🚀 **Fast Scraping**: Optimized timeouts and reduced delays
- 🎯 **Smart Filtering**: Only extracts company emails, skips personal emails
- 📊 **Flexible Options**: Choose max companies and email collection strategy
- 💾 **Multiple Export Formats**: CSV and JSON export
- 🌐 **Web Interface**: Easy-to-use web UI

## Deployment on Netlify

### Option 1: Deploy via Netlify UI

1. Fork or clone this repository
2. Go to [Netlify](https://netlify.com) and sign up/login
3. Click "New site from Git"
4. Connect your GitHub account and select this repository
5. Build settings:
   - Build command: `pip install -r requirements.txt`
   - Publish directory: `.`
6. Click "Deploy site"

### Option 2: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod
```

## Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Usage

1. **Search Options**:
   - Enter search term (e.g., "realtor", "restaurant")
   - Select max companies (5-500)
   - Choose email collection strategy:
     - **Limited**: First 10 emails per company
     - **All Available**: Every email found per company

2. **Results**:
   - View extracted emails in real-time
   - Export to CSV or JSON
   - Track scraping progress

## Configuration

Key settings in `app.py`:
- `DEFAULT_MAX_COMPANIES`: Default company limit
- `DEFAULT_DELAY_BETWEEN_REQUESTS`: Delay between requests (0.5s)
- `DEFAULT_ELEMENT_TIMEOUT`: Element search timeout (5s)

## Notes

- **Selenium Required**: Uses Chrome WebDriver for scraping
- **Rate Limiting**: Built-in delays to respect Trustpilot
- **Email Filtering**: Automatically filters out personal email domains
- **Error Handling**: Robust error handling and progress tracking

## License

MIT License
