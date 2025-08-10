# 🚀 Trustpilot Email Scraper

A powerful web scraping tool that extracts company email addresses from Trustpilot reviews. Built with Python, Flask, and Selenium for robust data extraction.

## ✨ Features

- **🔐 Password Protection**: Secure access with customizable password
- **🎨 GOCONNECT Branding**: Professional login interface with company branding
- **Smart Email Extraction**: Automatically identifies and extracts company email addresses
- **Company Filtering**: Skips companies without email addresses for clean results
- **Flexible Scraping Options**: Choose between limited (first 10) or all available emails per company
- **Sector-based Search**: Filter companies by business sector
- **CSV Export**: Download results in spreadsheet format
- **Real-time Progress**: Live updates during scraping process
- **Web Interface**: User-friendly browser-based application
- **Speed Optimized**: Reduced delays and timeouts for faster scraping

## 🚀 Deployment on Railway

This application is configured for deployment on Railway, a modern platform for deploying full-stack applications.

### **Prerequisites**
- [Railway Account](https://railway.app/)
- [GitHub Repository](https://github.com/olawanle/trustpilot-scraper)

### **Deployment Steps**

1. **Fork/Clone Repository**
   ```bash
   git clone https://github.com/olawanle/trustpilot-scraper.git
   cd trustpilot-email-scraper
   ```

2. **Connect to Railway**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Automatic Deployment**
   - Railway will automatically detect the Python application
   - Build and deploy using the configuration in `railway.json`
   - The app will be available at your Railway domain

4. **Environment Variables** (Optional)
   - `PORT`: Automatically set by Railway
   - `SECRET_KEY`: Change the default secret key in production

### **Railway Configuration**

The application includes:
- **`railway.json`**: Railway-specific deployment configuration
- **`Procfile`**: Process management for Railway
- **`runtime.txt`**: Python version specification
- **`requirements.txt`**: Python dependencies

## 🔐 Security Features

- **Password Protection**: Default password is `olawanle` (change in production)
- **Session Management**: Secure Flask sessions
- **Route Protection**: All API endpoints require authentication
- **Logout Functionality**: Secure session termination

## 🛠️ Local Development

### **Prerequisites**
- Python 3.9+
- Chrome/Chromium browser
- Git

### **Installation**

1. **Clone Repository**
   ```bash
   git clone https://github.com/olawanle/trustpilot-scraper.git
   cd trustpilot-email-scraper
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Application**
   - Open browser: `http://localhost:5000`
   - Login with password: `olawanle`

## 📱 Usage

### **Basic Search**
1. Enter company name or search term
2. Select sector (optional)
3. Choose maximum companies to scrape
4. Select email scraping option (limited vs. all)
5. Click "Search" to start scraping

### **Advanced Options**
- **Sector Selection**: Pre-defined business sectors with relevant search terms
- **Company Limits**: Control how many companies to process (5-500)
- **Email Scraping**: Choose between first 10 emails or all available emails per company

### **Export Options**
- **CSV Export**: Download results in spreadsheet format
- **JSON Export**: Download raw data for further processing

## 🔧 Configuration

### **Default Settings**
- **Max Companies**: 10 (configurable 5-500)
- **Delay Between Requests**: 0.5 seconds
- **Page Load Timeout**: 15 seconds
- **Element Timeout**: 5 seconds
- **Chrome Headless**: Enabled for production

### **Customization**
Edit the configuration variables in `app.py`:
```python
DEFAULT_MAX_COMPANIES = 10
DEFAULT_DELAY_BETWEEN_REQUESTS = 0.5
DEFAULT_PAGE_LOAD_TIMEOUT = 15
DEFAULT_ELEMENT_TIMEOUT = 5
```

## 📊 Supported Sectors

- **Real Estate**: Real estate agencies, property management, realtors
- **Finance & Banking**: Banks, investment firms, insurance companies
- **Healthcare**: Hospitals, clinics, medical practices, pharmacies
- **Technology**: Software companies, IT services, technology firms
- **Retail & E-commerce**: Online stores, retail chains, marketplaces
- **Custom Search**: User-defined search terms for any industry

## 🚨 Important Notes

- **Rate Limiting**: Respect Trustpilot's terms of service
- **Browser Requirements**: Chrome/Chromium browser required for Selenium
- **Production Security**: Change default secret key and password in production
- **Resource Usage**: Large scraping jobs may consume significant resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect Trustpilot's terms of service and use responsibly.

## 🆘 Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/olawanle/trustpilot-scraper/issues)
- Review the configuration and requirements
- Ensure Chrome/Chromium is properly installed

---

**Built with ❤️ using Python, Flask, and Selenium**
