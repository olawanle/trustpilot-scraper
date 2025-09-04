from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import csv
import io
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import threading
from queue import Queue
import os
from functools import wraps
# Default values for configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = int(os.environ.get('PORT', 5000))  # Railway will provide PORT environment variable
FLASK_DEBUG = False  # Set to False for production
DEFAULT_MAX_COMPANIES = 10
DEFAULT_DELAY_BETWEEN_REQUESTS = 0.5
DEFAULT_PAGE_LOAD_TIMEOUT = 15
DEFAULT_ELEMENT_TIMEOUT = 5
CHROME_HEADLESS = True
CHROME_NO_SANDBOX = True
CHROME_DISABLE_DEV_SHM = True
CHROME_DISABLE_GPU = True
CHROME_WINDOW_SIZE = "1920,1080"
TRUSTPILOT_BASE_URL = "https://www.trustpilot.com"
TRUSTPILOT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Change this in production
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for progress tracking
scraping_progress = {}
scraping_queue = Queue()

def login_required(view_function):
    """Simple session-based login required decorator"""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            # For API requests, return 401 JSON; for others, redirect to login
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        return view_function(*args, **kwargs)
    return wrapped_view

class TrustpilotScraper:
    def __init__(self):
        self.base_url = TRUSTPILOT_BASE_URL
        self.headers = {
            'User-Agent': TRUSTPILOT_USER_AGENT
        }
        self.driver = None
    
    def setup_driver(self):
        """Setup Chrome driver with options"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        chrome_options = Options()
        if CHROME_HEADLESS:
            chrome_options.add_argument("--headless")
        if CHROME_NO_SANDBOX:
            chrome_options.add_argument("--no-sandbox")
        if CHROME_DISABLE_DEV_SHM:
            chrome_options.add_argument("--disable-dev-shm-usage")
        if CHROME_DISABLE_GPU:
            chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={CHROME_WINDOW_SIZE}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return self.driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            return None
    
    def cleanup_driver(self):
        """Clean up the driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
            except:
                pass
    
    def clean_company_name(self, raw_name):
        """Clean up company name by removing extra text"""
        if not raw_name:
            return ""
        
        # Remove review counts, ratings, and URLs
        clean_name = re.sub(r'www\.[^\s]+', '', raw_name)
        clean_name = re.sub(r'[0-9]+\.[0-9]+', '', clean_name)
        clean_name = re.sub(r'[0-9,]+\s*reviews?', '', clean_name)
        clean_name = re.sub(r'[0-9,]+\s*ratings?', '', clean_name)
        
        # Remove location patterns (e.g., "27 Union Square West, New York, United States")
        clean_name = re.sub(r'\d+\s+[A-Za-z\s]+,?\s*[A-Za-z\s]+,?\s*[A-Za-z\s]+$', '', clean_name)
        
        # Remove remaining numbers and special characters
        clean_name = re.sub(r'[0-9,]+', '', clean_name)
        clean_name = re.sub(r'[^\w\s\-&]', '', clean_name)  # Keep only alphanumeric, spaces, hyphens, and ampersands
        
        # Additional cleaning for common patterns
        clean_name = re.sub(r'\s+', ' ', clean_name)  # Normalize whitespace
        clean_name = re.sub(r'^[^\w]*', '', clean_name)  # Remove leading non-word chars
        clean_name = re.sub(r'[^\w]*$', '', clean_name)  # Remove trailing non-word chars
        
        return clean_name.strip()
    
    def search_companies(self, search_term, max_companies=10):
        """Search for companies on Trustpilot with improved sector targeting"""
        try:
            # Enhanced search terms for better sector targeting
            enhanced_search_terms = self.get_enhanced_search_terms(search_term)
            companies = []
            
            for search_term_variant in enhanced_search_terms:
                if len(companies) >= max_companies:
                    break
                    
                search_url = f"{self.base_url}/search?query={search_term_variant}"
                response = requests.get(search_url, headers=self.headers, timeout=DEFAULT_PAGE_LOAD_TIMEOUT)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for company links in search results
                company_links = soup.find_all('a', href=re.compile(r'/review/'))
                
                for link in company_links:
                    if len(companies) >= max_companies:
                        break
                        
                    company_name = link.get_text(strip=True)
                    company_url = self.base_url + link['href'] if link['href'].startswith('/') else link['href']
                    
                    # Clean up company name
                    clean_name = self.clean_company_name(company_name)
                    if clean_name and len(clean_name) > 2:  # Only add if name is meaningful
                        # Check if company is already in the list
                        if not any(c['name'] == clean_name for c in companies):
                            companies.append({
                                'name': clean_name,
                                'url': company_url,
                                'raw_name': company_name,  # Keep original for debugging
                                'search_term_used': search_term_variant
                            })
            
            logger.info(f"Found {len(companies)} companies for search term: {search_term}")
            return companies
            
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return []
    
    def get_enhanced_search_terms(self, base_term):
        """Generate enhanced search terms for better sector targeting"""
        # Real estate specific enhancements
        real_estate_terms = [
            f"{base_term} real estate",
            f"{base_term} property",
            f"{base_term} realtor",
            f"{base_term} estate agent",
            f"{base_term} property management",
            f"{base_term} real estate agency",
            f"{base_term} property investment",
            f"{base_term} real estate broker",
            f"{base_term} property developer",
            f"{base_term} real estate consultant"
        ]
        
        # General business enhancements
        general_terms = [
            base_term,
            f"{base_term} company",
            f"{base_term} business",
            f"{base_term} services",
            f"{base_term} ltd",
            f"{base_term} inc",
            f"{base_term} corp"
        ]
        
        # Combine and return unique terms
        all_terms = real_estate_terms + general_terms
        return list(dict.fromkeys(all_terms))  # Remove duplicates while preserving order
    
    def safe_find_elements(self, driver, by, value, timeout=DEFAULT_ELEMENT_TIMEOUT):
        """Safely find elements with timeout and retry logic"""
        try:
            wait = WebDriverWait(driver, timeout)
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return elements
        except (TimeoutException, WebDriverException) as e:
            logger.warning(f"Timeout finding elements {by}={value}: {e}")
            return []
    
    def scrape_company_page(self, company_url):
        """Scrape company page for company contact information (emails only)"""
        try:
            if not self.driver:
                self.setup_driver()
            
            if not self.driver:
                return []
            
            self.driver.get(company_url)
            time.sleep(1)  # Reduced wait time for faster scraping
            
            # Look for company emails only
            company_emails = []
            
            try:
                # Look for contact section with better error handling
                contact_sections = self.safe_find_elements(
                    self.driver, 
                    By.XPATH, 
                    "//*[contains(text(), 'Contact') or contains(text(), 'contact') or contains(text(), 'Email') or contains(text(), 'email')]"
                )
                
                for section in contact_sections:
                    try:
                        # Get parent element safely
                        parent = section.find_element(By.XPATH, "./..")
                        text = parent.text
                        
                        # Extract emails using regex - focus on company emails only
                        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                        
                        # Filter out common personal email domains and only keep company emails
                        valid_company_emails = [email for email in emails if not self.is_personal_email(email)]
                        company_emails.extend(valid_company_emails)
                        
                    except StaleElementReferenceException:
                        continue  # Skip stale elements
                    except Exception as e:
                        logger.debug(f"Error processing contact section: {e}")
                        continue
                
                # Look for contact forms and additional contact info
                contact_forms = self.safe_find_elements(
                    self.driver, 
                    By.XPATH, 
                    "//*[contains(@class, 'contact') or contains(@class, 'email') or contains(@placeholder, 'email')]"
                )
                
                for form in contact_forms:
                    try:
                        text = form.text
                        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                        valid_company_emails = [email for email in emails if not self.is_personal_email(email)]
                        company_emails.extend(valid_company_emails)
                    except Exception as e:
                        logger.debug(f"Error processing contact form: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error extracting contact info: {e}")
            
            # Remove duplicates - no limit on emails per company
            unique_emails = list(set(company_emails))
            return unique_emails
            
        except Exception as e:
            logger.error(f"Error scraping company page: {e}")
            return []
    
    def is_personal_email(self, email):
        """Check if email is likely personal rather than company email"""
        personal_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'aol.com', 'icloud.com', 'protonmail.com', 'mail.com'
        ]
        domain = email.split('@')[-1].lower()
        return domain in personal_domains
    
    def scrape_reviews_for_emails(self, company_url, max_reviews=50):
        """Scrape reviews for potential email addresses"""
        try:
            if not self.driver:
                self.setup_driver()
            
            if not self.driver:
                return []
            
            # Go to reviews page
            reviews_url = company_url.replace('/review/', '/reviews/')
            self.driver.get(reviews_url)
            time.sleep(3)
            
            emails = []
            
            # Scroll through reviews to load more content
            for _ in range(3):
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                except:
                    break
            
            # Extract all text content
            page_text = self.driver.page_source
            soup = BeautifulSoup(page_text, 'html.parser')
            
            # Find all review text with better pattern matching
            review_elements = soup.find_all(['p', 'div', 'span'], class_=re.compile(r'review|comment|text|content'))
            
            for element in review_elements:
                text = element.get_text()
                # Extract emails from review text
                found_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
                emails.extend(found_emails)
                
                # Limit the number of reviews processed
                if len(emails) >= max_reviews:
                    break
            
            return list(set(emails))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error scraping reviews: {e}")
            return []

scraper = TrustpilotScraper()

def background_scraping_task(search_id, search_term, max_companies, scrape_all_emails=False):
    """Background task for scraping"""
    try:
        scraping_progress[search_id] = {
            'status': 'running',
            'progress': 0,
            'total_companies': 0,
            'companies_processed': 0,
            
            'companies_found': 0,
            'emails_found': 0,
            'results': [],
            'search_term': search_term
        }
        
        # Search for companies
        companies = scraper.search_companies(search_term, max_companies)
        scraping_progress[search_id]['total_companies'] = len(companies)
        scraping_progress[search_id]['companies_found'] = len(companies)
        
        if not companies:
            scraping_progress[search_id]['status'] = 'completed'
            scraping_progress[search_id]['progress'] = 100
            return
        
        # Process each company
        for i, company in enumerate(companies):
            if scraping_progress[search_id]['status'] == 'cancelled':
                break
                
            scraping_progress[search_id]['companies_processed'] = i + 1
            scraping_progress[search_id]['progress'] = int((i + 1) / len(companies) * 100)
            
            logger.info(f"Processing company {i+1}/{len(companies)}: {company['name']}")
            
            # Get company contact info (emails only)
            if scrape_all_emails:
                # Scrape all available emails
                company_emails = scraper.scrape_company_page(company['url'])
            else:
                # Limit to first 10 emails per company
                company_emails = scraper.scrape_company_page(company['url'])[:10]
            
            # Only include companies that have at least one email
            if company_emails:
                # Update email count
                scraping_progress[search_id]['emails_found'] += len(company_emails)
                
                result = {
                    'name': company['name'],
                    'url': company['url'],
                    'raw_name': company.get('raw_name', ''),
                    'company_emails': company_emails,
                    'total_emails': len(company_emails),
                    'sector': search_term,
                    'scraped_at': datetime.now().isoformat()
                }
                
                scraping_progress[search_id]['results'].append(result)
            else:
                logger.info(f"Skipping company {company['name']} - no emails found")
            
            # Reduced delay for faster scraping
            time.sleep(0.5)
        
        scraping_progress[search_id]['status'] = 'completed'
        scraping_progress[search_id]['progress'] = 100
        
        # Clean up driver after completion
        scraper.cleanup_driver()
        
    except Exception as e:
        logger.error(f"Error in background scraping: {e}")
        scraping_progress[search_id]['status'] = 'error'
        scraping_progress[search_id]['error'] = str(e)
        # Clean up driver on error
        scraper.cleanup_driver()

@app.route('/')
@login_required
def index():
    """Main page - requires login"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'olawanle':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/search', methods=['POST'])
@login_required
def start_search():
    try:
        data = request.get_json()
        search_term = data.get('search_term', '').strip()
        max_companies = data.get('max_companies', DEFAULT_MAX_COMPANIES)
        scrape_all_emails = data.get('scrape_all_emails', False)
        
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        # Generate unique search ID
        search_id = f"search_{int(time.time())}"
        
        logger.info(f"Starting search: {search_term} (max companies: {max_companies}, scrape all emails: {scrape_all_emails})")
        
        # Start background scraping task
        thread = threading.Thread(
            target=background_scraping_task,
            args=(search_id, search_term, max_companies, scrape_all_emails)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'search_id': search_id,
            'message': 'Search started successfully',
            'search_term': search_term
        })
        
    except Exception as e:
        logger.error(f"Error starting search: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress/<search_id>')
@login_required
def get_progress(search_id):
    """Get progress of a specific search"""
    if search_id not in scraping_progress:
        return jsonify({'error': 'Search ID not found'}), 404
    
    return jsonify(scraping_progress[search_id])

@app.route('/api/results/<search_id>')
@login_required
def get_results(search_id):
    """Get results of a completed search"""
    if search_id not in scraping_progress:
        return jsonify({'error': 'Search ID not found'}), 404
    
    progress = scraping_progress[search_id]
    if progress['status'] != 'completed':
        return jsonify({'error': 'Search not completed yet'}), 400
    
    return jsonify({
        'search_term': progress.get('search_term', ''),
        'companies_found': progress['companies_found'],
        'emails_found': progress['emails_found'],
        'results': progress['results']
    })

@app.route('/api/cancel/<search_id>')
@login_required
def cancel_search(search_id):
    """Cancel a running search"""
    if search_id not in scraping_progress:
        return jsonify({'error': 'Search ID not found'}), 404
    
    scraping_progress[search_id]['status'] = 'cancelled'
    return jsonify({'message': 'Search cancelled successfully'})

@app.route('/api/export/csv/<search_id>')
@login_required
def export_csv(search_id):
    """Export results to CSV"""
    if search_id not in scraping_progress:
        return jsonify({'error': 'Search ID not found'}), 404
    
    progress = scraping_progress[search_id]
    if progress['status'] != 'completed':
        return jsonify({'error': 'Search not completed yet'}), 400
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Company Name', 'Company URL', 'Company Contact Info', 
        'Total Emails', 'Sector', 'Scraped At'
    ])
    
    # Write data
    for company in progress['results']:
        writer.writerow([
            company['name'],
            company['url'],
            '; '.join(company['company_emails']),
            company['total_emails'],
            company.get('sector', ''),
            company.get('scraped_at', '')
        ])
    
    output.seek(0)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"trustpilot_emails_{search_id}_{timestamp}.csv"
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/export/json/<search_id>')
@login_required
def export_json(search_id):
    """Export results to JSON"""
    if search_id not in scraping_progress:
        return jsonify({'error': 'Search ID not found'}), 404
    
    progress = scraping_progress[search_id]
    if progress['status'] != 'completed':
        return jsonify({'error': 'Search not completed yet'}), 400
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"trustpilot_emails_{search_id}_{timestamp}.json"
    
    return send_file(
        io.BytesIO(json.dumps(progress, indent=2).encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/sectors')
@login_required
def get_sectors():
    """Get available sectors for search suggestions"""
    sectors = {
        'real_estate': {
            'name': 'Real Estate',
            'search_terms': ['real estate', 'property', 'realtor', 'estate agent', 'property management'],
            'description': 'Real estate agencies, property management, realtors, and property services'
        },
        'finance': {
            'name': 'Finance & Banking',
            'search_terms': ['finance', 'banking', 'investment', 'insurance', 'mortgage'],
            'description': 'Banks, investment firms, insurance companies, and financial services'
        },
        'healthcare': {
            'name': 'Healthcare',
            'search_terms': ['healthcare', 'medical', 'hospital', 'clinic', 'pharmacy'],
            'description': 'Hospitals, clinics, medical practices, and healthcare services'
        },
        'technology': {
            'name': 'Technology',
            'search_terms': ['technology', 'software', 'IT', 'digital', 'tech'],
            'description': 'Software companies, IT services, and technology firms'
        },
        'retail': {
            'name': 'Retail & E-commerce',
            'search_terms': ['retail', 'ecommerce', 'online store', 'shopping', 'marketplace'],
            'description': 'Online stores, retail chains, and e-commerce platforms'
        },
        'custom': {
            'name': 'Custom Search',
            'search_terms': [],
            'description': 'Enter your own search terms for any industry or company type'
        }
    }
    return jsonify(sectors)

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Trustpilot Email Scraper is running'})

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)
