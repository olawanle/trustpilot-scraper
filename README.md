# 🚀 Trustpilot Email Scraper

A powerful web scraping tool that extracts company email addresses from Trustpilot reviews. Built with Python, Flask, and Selenium for robust data extraction.

## ✨ Features

- **Smart Email Extraction**: Automatically identifies and extracts company email addresses
- **Company Filtering**: Skips companies without email addresses for clean results
- **Flexible Scraping Options**: Choose between limited (first 10) or all available emails per company
- **Sector-based Search**: Filter companies by business sector
- **CSV Export**: Download results in spreadsheet format
- **Real-time Progress**: Live updates during scraping process
- **Web Interface**: User-friendly browser-based application
- **Speed Optimized**: Reduced delays for faster scraping

## 🏗️ Architecture

- **Backend**: Python Flask application with Selenium WebDriver
- **Frontend**: Modern HTML/CSS/JavaScript interface
- **Scraping Engine**: Automated browser automation for data extraction
- **Data Processing**: Regex-based email validation and deduplication

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Chrome browser
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/trustpilot-email-scraper.git
   cd trustpilot-email-scraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📖 Usage

### Basic Search
1. Enter a search term (e.g., "realtor", "restaurant")
2. Select maximum number of companies to scrape
3. Choose email scraping mode:
   - **Limited**: First 10 emails per company
   - **All Available**: Every email found per company
4. Click "Start Search" and wait for results

### Advanced Options
- **Sector Selection**: Filter by business category
- **Company Limit**: Set maximum companies to process
- **Real-time Monitoring**: Watch progress in real-time

### Export Results
- **CSV Download**: Export all results to spreadsheet
- **Data Format**: Company name, URL, emails, sector, timestamp

## 🔧 Configuration

### Environment Variables
- `DEFAULT_MAX_COMPANIES`: Maximum companies to scrape (default: 50)
- `DEFAULT_DELAY_BETWEEN_REQUESTS`: Delay between requests (default: 0.5s)
- `DEFAULT_PAGE_LOAD_TIMEOUT`: Page load timeout (default: 15s)

### Customization
- Modify `config.py` for application settings
- Adjust delays in `app.py` for different scraping speeds
- Customize email regex patterns for specific formats

## 🌐 Deployment

### Netlify (Static Frontend)
The web interface is deployed on Netlify:
- **Live URL**: https://trustscraper.netlify.app
- **Admin Panel**: https://app.netlify.com/projects/trustscraper

### Local Backend
The Python scraper runs locally and requires:
- Python environment
- Chrome browser
- Selenium WebDriver

## 📊 Data Structure

### Company Information
```json
{
  "name": "Company Name",
  "url": "https://www.trustpilot.com/review/company",
  "company_emails": ["email@company.com"],
  "total_emails": 1,
  "sector": "business_sector",
  "scraped_at": "2025-08-09T18:46:55.345821"
}
```

### CSV Export Format
- Company Name
- Company URL
- Company Emails
- Total Emails
- Sector
- Scraped At

## 🛠️ Development

### Project Structure
```
trustpilot-email-scraper/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── templates/
│   └── index.html        # Web interface
├── venv/                 # Virtual environment
├── netlify.toml          # Netlify configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Key Components
- **TrustpilotScraper**: Core scraping logic
- **Flask Routes**: API endpoints for search operations
- **Background Tasks**: Asynchronous scraping with threading
- **Web Interface**: User-friendly frontend

## ⚠️ Important Notes

- **Rate Limiting**: Respect Trustpilot's terms of service
- **Legal Compliance**: Ensure compliance with local laws and website terms
- **Data Usage**: Use extracted data responsibly and ethically
- **Browser Requirements**: Chrome browser required for Selenium automation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check this README for usage instructions
- **Community**: Join discussions in GitHub Discussions

## 🔄 Updates

### Recent Changes
- ✅ Added "Scrape All Emails" option
- ✅ Optimized scraping speed
- ✅ Improved email filtering
- ✅ Enhanced UI/UX
- ✅ Netlify deployment ready

### Roadmap
- [ ] API rate limiting
- [ ] Multiple search term support
- [ ] Advanced filtering options
- [ ] Data analytics dashboard
- [ ] Mobile-responsive design

---

**Built with ❤️ using Python, Flask, and Selenium**
