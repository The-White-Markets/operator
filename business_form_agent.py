#!/usr/bin/env python3
"""
Business Contact Form Automation Agent
Finds a business website and fills out their contact form
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import re
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class BusinessFormAgent:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--headless")  # Uncomment for headless mode
        
        # Automatically download and setup ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def search_business_website(self, business_name):
        """Search for business website using Google"""
        print(f"🔍 Searching for: {business_name}")
        
        # Format search query
        search_query = f"{business_name} official website"
        google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        try:
            self.driver.get(google_url)
            time.sleep(2)
            
            # Find first organic result
            results = self.driver.find_elements(By.CSS_SELECTOR, "div.g a[href]")
            
            for result in results[:3]:  # Check first 3 results
                href = result.get_attribute("href")
                if href and self.is_valid_business_url(href, business_name):
                    print(f"✅ Found website: {href}")
                    return href
                    
        except Exception as e:
            print(f"❌ Search error: {e}")
            
        return None
    
    def is_valid_business_url(self, url, business_name):
        """Check if URL seems to be the business's official website"""
        if not url or url.startswith(('javascript:', 'mailto:')):
            return False
            
        # Skip non-business sites
        skip_domains = ['google.com', 'facebook.com', 'yelp.com', 'tripadvisor.com', 
                       'opentable.com', 'grubhub.com', 'doordash.com', 'ubereats.com']
        
        domain = urlparse(url).netloc.lower()
        for skip in skip_domains:
            if skip in domain:
                return False
                
        return True
    
    def find_contact_page(self, base_url):
        """Find contact page URL"""
        print(f"🔍 Looking for contact page on: {base_url}")
        
        try:
            self.driver.get(base_url)
            time.sleep(3)
            
            # Common contact page patterns
            contact_patterns = [
                "//a[contains(translate(text(), 'CONTACT', 'contact'), 'contact')]",
                "//a[contains(translate(@href, 'CONTACT', 'contact'), 'contact')]",
                "//a[contains(translate(text(), 'ABOUT', 'about'), 'about')]",
                "//a[contains(translate(@href, 'ABOUT', 'about'), 'about')]",
                "//a[contains(translate(text(), 'RESERVATION', 'reservation'), 'reservation')]",
                "//a[contains(translate(@href, 'RESERVATION', 'reservation'), 'reservation')]"
            ]
            
            for pattern in contact_patterns:
                try:
                    elements = self.driver.find_elements(By.XPATH, pattern)
                    for element in elements:
                        href = element.get_attribute("href")
                        text = element.text.strip().lower()
                        
                        if href and any(word in text for word in ['contact', 'about', 'reservation']):
                            contact_url = urljoin(base_url, href)
                            print(f"📞 Found contact page: {contact_url}")
                            return contact_url
                except:
                    continue
                    
            # If no specific contact page, try the main page for forms
            print("📄 No specific contact page found, checking main page for forms")
            return base_url
            
        except Exception as e:
            print(f"❌ Error finding contact page: {e}")
            return base_url
    
    def find_and_fill_form(self, url, form_data):
        """Find contact form and fill it out"""
        print(f"📝 Looking for forms on: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            # Look for forms
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            if not forms:
                print("❌ No forms found on page")
                return False
                
            print(f"📋 Found {len(forms)} form(s)")
            
            # Try each form
            for i, form in enumerate(forms):
                print(f"🔄 Trying form {i+1}...")
                
                if self.fill_form_fields(form, form_data):
                    print("✅ Successfully filled form!")
                    return True
                    
            print("❌ Could not fill any forms")
            return False
            
        except Exception as e:
            print(f"❌ Error filling form: {e}")
            return False
    
    def fill_form_fields(self, form, form_data):
        """Fill individual form fields"""
        try:
            # Find input fields
            inputs = form.find_elements(By.TAG_NAME, "input")
            textareas = form.find_elements(By.TAG_NAME, "textarea")
            selects = form.find_elements(By.TAG_NAME, "select")
            
            filled_fields = 0
            
            # Fill text inputs
            for inp in inputs:
                input_type = inp.get_attribute("type") or "text"
                name = inp.get_attribute("name") or ""
                placeholder = inp.get_attribute("placeholder") or ""
                id_attr = inp.get_attribute("id") or ""
                
                # Skip hidden, submit, button inputs
                if input_type.lower() in ["hidden", "submit", "button"]:
                    continue
                
                field_text = f"{name} {placeholder} {id_attr}".lower()
                
                # Map form fields to data
                if any(word in field_text for word in ["name", "full", "first"]):
                    inp.clear()
                    inp.send_keys(form_data["name"])
                    filled_fields += 1
                    print(f"✓ Filled name field: {form_data['name']}")
                    
                elif any(word in field_text for word in ["email", "mail"]):
                    inp.clear()
                    inp.send_keys(form_data["email"])
                    filled_fields += 1
                    print(f"✓ Filled email field: {form_data['email']}")
                    
                elif any(word in field_text for word in ["phone", "tel"]):
                    inp.clear()
                    inp.send_keys(form_data["phone"])
                    filled_fields += 1
                    print(f"✓ Filled phone field: {form_data['phone']}")
            
            # Fill textareas (usually message/comment fields)
            for textarea in textareas:
                name = textarea.get_attribute("name") or ""
                placeholder = textarea.get_attribute("placeholder") or ""
                
                field_text = f"{name} {placeholder}".lower()
                
                if any(word in field_text for word in ["message", "comment", "inquiry", "details"]):
                    textarea.clear()
                    textarea.send_keys(form_data["message"])
                    filled_fields += 1
                    print(f"✓ Filled message field")
            
            if filled_fields > 0:
                print(f"📝 Filled {filled_fields} fields")
                
                # Try to submit
                submit_buttons = form.find_elements(By.CSS_SELECTOR, 
                    "input[type='submit'], button[type='submit'], button:not([type])")
                
                for button in submit_buttons:
                    button_text = button.text.strip().lower()
                    if any(word in button_text for word in ["submit", "send", "contact", ""]):
                        print("🚀 Attempting to submit form...")
                        button.click()
                        time.sleep(2)
                        return True
                        
            return filled_fields > 0
            
        except Exception as e:
            print(f"❌ Error filling form fields: {e}")
            return False
    
    def process_business(self, business_name, form_data):
        """Complete process: search → find contact → fill form"""
        print(f"\n🎯 Processing: {business_name}")
        print("=" * 50)
        
        # Step 1: Find website
        website = self.search_business_website(business_name)
        if not website:
            print("❌ Could not find business website")
            return False
            
        # Step 2: Find contact page
        contact_url = self.find_contact_page(website)
        
        # Step 3: Fill form
        success = self.find_and_fill_form(contact_url, form_data)
        
        if success:
            print("🎉 Successfully completed form submission!")
        else:
            print("❌ Failed to submit form")
            
        return success
    
    def close(self):
        """Clean up"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    # Test data for form filling
    form_data = {
        "name": "John Smith",
        "email": "john.smith@example.com", 
        "phone": "(555) 123-4567",
        "message": "Hi, I'm interested in making a reservation for dinner. Could you please let me know your availability for this weekend? Thank you!"
    }
    
    agent = BusinessFormAgent()
    
    try:
        # Test with Il Pastaio Beverly Hills
        success = agent.process_business("Il Pastaio Beverly Hills", form_data)
        
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        agent.close()

if __name__ == "__main__":
    main()