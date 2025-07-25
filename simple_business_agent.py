#!/usr/bin/env python3
"""
Simple Business Contact Form Agent (No Browser Required)
Finds a business website using web search and attempts to identify contact forms
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import re
from urllib.parse import urljoin, urlparse
import urllib.parse

class SimpleBusinessAgent:
    def __init__(self):
        self.session = requests.Session()
        # Set a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_business_website(self, business_name):
        """Search for business website using DuckDuckGo (no API key needed)"""
        print(f"🔍 Searching for: {business_name}")
        
        try:
            # Use DuckDuckGo search
            search_query = f"{business_name} official website"
            search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(search_query)}"
            
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find search results
            results = soup.find_all('a', class_='result__a')
            
            for result in results[:5]:  # Check first 5 results
                href = result.get('href')
                if href and self.is_valid_business_url(href, business_name):
                    print(f"✅ Found website: {href}")
                    return href
                    
            # Fallback: try some common website patterns
            business_clean = business_name.lower().replace(' ', '').replace(',', '')
            common_patterns = [
                f"https://{business_clean}.com",
                f"https://www.{business_clean}.com",
                f"https://{business_clean.replace('restaurant', '').replace('cafe', '').replace('bistro', '').strip()}.com"
            ]
            
            for url in common_patterns:
                try:
                    response = self.session.head(url, timeout=5)
                    if response.status_code == 200:
                        print(f"✅ Found website via pattern matching: {url}")
                        return url
                except:
                    continue
                    
        except Exception as e:
            print(f"❌ Search error: {e}")
            
        return None
    
    def is_valid_business_url(self, url, business_name):
        """Check if URL seems to be the business's official website"""
        if not url or url.startswith(('javascript:', 'mailto:')):
            return False
            
        # Skip non-business sites
        skip_domains = ['google.com', 'facebook.com', 'yelp.com', 'tripadvisor.com', 
                       'opentable.com', 'grubhub.com', 'doordash.com', 'ubereats.com',
                       'duckduckgo.com', 'wikipedia.org']
        
        domain = urlparse(url).netloc.lower()
        for skip in skip_domains:
            if skip in domain:
                return False
                
        return True
    
    def find_contact_info_and_forms(self, base_url):
        """Find contact information and forms on the website"""
        print(f"🔍 Analyzing website: {base_url}")
        
        contact_info = {
            'contact_page': None,
            'forms_found': [],
            'phone': None,
            'email': None,
            'address': None
        }
        
        try:
            # Get main page
            response = self.session.get(base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract basic contact info
            contact_info['phone'] = self.extract_phone(soup)
            contact_info['email'] = self.extract_email(soup)
            contact_info['address'] = self.extract_address(soup)
            
            # Look for contact page links
            contact_links = []
            for link in soup.find_all('a', href=True):
                text = link.get_text().strip().lower()
                href = link['href']
                
                if any(word in text for word in ['contact', 'reservation', 'book', 'inquiry']):
                    contact_url = urljoin(base_url, href)
                    contact_links.append((text, contact_url))
            
            # Check main page for forms
            forms = soup.find_all('form')
            if forms:
                print(f"📋 Found {len(forms)} form(s) on main page")
                for i, form in enumerate(forms):
                    form_info = self.analyze_form(form, f"{base_url}#form{i}")
                    if form_info:
                        contact_info['forms_found'].append(form_info)
            
            # Check contact pages
            for text, contact_url in contact_links[:3]:  # Check first 3 contact links
                print(f"📞 Checking contact page: {text} -> {contact_url}")
                
                try:
                    contact_response = self.session.get(contact_url, timeout=10)
                    contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                    
                    # Update contact info from contact page
                    phone = self.extract_phone(contact_soup)
                    email = self.extract_email(contact_soup)
                    address = self.extract_address(contact_soup)
                    
                    if phone and not contact_info['phone']:
                        contact_info['phone'] = phone
                    if email and not contact_info['email']:
                        contact_info['email'] = email
                    if address and not contact_info['address']:
                        contact_info['address'] = address
                    
                    # Look for forms on contact page
                    contact_forms = contact_soup.find_all('form')
                    if contact_forms:
                        print(f"📋 Found {len(contact_forms)} form(s) on contact page")
                        contact_info['contact_page'] = contact_url
                        
                        for i, form in enumerate(contact_forms):
                            form_info = self.analyze_form(form, f"{contact_url}#form{i}")
                            if form_info:
                                contact_info['forms_found'].append(form_info)
                                
                except Exception as e:
                    print(f"❌ Error checking contact page {contact_url}: {e}")
                    continue
            
        except Exception as e:
            print(f"❌ Error analyzing website: {e}")
            
        return contact_info
    
    def analyze_form(self, form, form_url):
        """Analyze a form to see if it's suitable for contact"""
        form_info = {
            'url': form_url,
            'method': form.get('method', 'get').lower(),
            'action': form.get('action', ''),
            'fields': [],
            'submit_text': ''
        }
        
        # Find input fields
        inputs = form.find_all(['input', 'textarea', 'select'])
        contact_field_count = 0
        
        for inp in inputs:
            field_type = inp.get('type', 'text')
            name = inp.get('name', '')
            placeholder = inp.get('placeholder', '')
            id_attr = inp.get('id', '')
            
            if field_type in ['hidden', 'submit', 'button']:
                if field_type == 'submit':
                    form_info['submit_text'] = inp.get('value', '')
                continue
                
            field_text = f"{name} {placeholder} {id_attr}".lower()
            
            field_info = {
                'type': field_type,
                'name': name,
                'placeholder': placeholder,
                'id': id_attr,
                'tag': inp.name
            }
            
            # Identify field purpose
            if any(word in field_text for word in ['name', 'full', 'first']):
                field_info['purpose'] = 'name'
                contact_field_count += 1
            elif any(word in field_text for word in ['email', 'mail']):
                field_info['purpose'] = 'email'
                contact_field_count += 1
            elif any(word in field_text for word in ['phone', 'tel']):
                field_info['purpose'] = 'phone'
                contact_field_count += 1
            elif any(word in field_text for word in ['message', 'comment', 'inquiry']):
                field_info['purpose'] = 'message'
                contact_field_count += 1
            else:
                field_info['purpose'] = 'other'
            
            form_info['fields'].append(field_info)
        
        # Find submit button
        submit_buttons = form.find_all(['input', 'button'], type=['submit', None])
        for button in submit_buttons:
            if button.name == 'button' or button.get('type') == 'submit':
                form_info['submit_text'] = button.get_text() or button.get('value', '')
                break
        
        # Only return forms that look like contact forms
        if contact_field_count >= 2:  # At least 2 contact-related fields
            return form_info
        
        return None
    
    def extract_phone(self, soup):
        """Extract phone number from page"""
        text = soup.get_text()
        # Look for phone patterns
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        return None
    
    def extract_email(self, soup):
        """Extract email from page"""
        text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        
        # Filter out common non-contact emails
        skip_emails = ['noreply', 'no-reply', 'admin', 'webmaster', 'info@example']
        for email in matches:
            if not any(skip in email.lower() for skip in skip_emails):
                return email
        return matches[0] if matches else None
    
    def extract_address(self, soup):
        """Extract address from page"""
        # Look for address patterns in text
        text = soup.get_text()
        
        # Simple address detection - look for street + city patterns
        address_indicators = ['street', 'st', 'avenue', 'ave', 'boulevard', 'blvd', 'drive', 'dr']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.strip().lower()
            if any(indicator in line_lower for indicator in address_indicators):
                # Try to get 2-3 lines that might form an address
                address_lines = []
                for j in range(max(0, i-1), min(len(lines), i+3)):
                    clean_line = lines[j].strip()
                    if clean_line and len(clean_line) > 5:
                        address_lines.append(clean_line)
                
                if address_lines:
                    return ' '.join(address_lines[:2])  # Take first 2 relevant lines
        
        return None
    
    def process_business(self, business_name):
        """Complete process: search → analyze → report"""
        print(f"\n🎯 Processing: {business_name}")
        print("=" * 50)
        
        # Step 1: Find website
        website = self.search_business_website(business_name)
        if not website:
            print("❌ Could not find business website")
            return None
            
        # Step 2: Analyze website
        contact_info = self.find_contact_info_and_forms(website)
        
        # Step 3: Report findings
        self.report_findings(business_name, website, contact_info)
        
        return contact_info
    
    def report_findings(self, business_name, website, contact_info):
        """Generate a report of findings"""
        print(f"\n📊 REPORT FOR: {business_name}")
        print("=" * 50)
        print(f"🌐 Website: {website}")
        
        if contact_info['phone']:
            print(f"📞 Phone: {contact_info['phone']}")
        
        if contact_info['email']:
            print(f"📧 Email: {contact_info['email']}")
            
        if contact_info['address']:
            print(f"📍 Address: {contact_info['address']}")
        
        if contact_info['contact_page']:
            print(f"📞 Contact Page: {contact_info['contact_page']}")
        
        if contact_info['forms_found']:
            print(f"\n📋 CONTACT FORMS FOUND: {len(contact_info['forms_found'])}")
            for i, form in enumerate(contact_info['forms_found'], 1):
                print(f"\n  Form {i}:")
                print(f"    URL: {form['url']}")
                print(f"    Method: {form['method'].upper()}")
                print(f"    Submit: {form['submit_text']}")
                print(f"    Fields:")
                for field in form['fields']:
                    if field['purpose'] != 'other':
                        print(f"      - {field['purpose'].title()}: {field['name']} ({field['type']})")
                        
            print(f"\n✅ Found {len(contact_info['forms_found'])} contact form(s)!")
            print("💡 These forms could be automated with Selenium or similar tools.")
        else:
            print("\n❌ No suitable contact forms found")
            print("💡 Try checking manually or contact via phone/email if available")

def main():
    print("🤖 Simple Business Contact Agent")
    print("=" * 40)
    
    agent = SimpleBusinessAgent()
    
    # Test with Il Pastaio Beverly Hills
    result = agent.process_business("Il Pastaio Beverly Hills")
    
    if result and result['forms_found']:
        print(f"\n🎉 SUCCESS! Found {len(result['forms_found'])} contact form(s)")
    elif result:
        print(f"\n📞 PARTIAL SUCCESS! Found contact info but no forms")
    else:
        print(f"\n❌ Could not find business information")

if __name__ == "__main__":
    main()