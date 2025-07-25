#!/usr/bin/env python3
"""
Complete Business Contact Form Agent
Finds a business website and actually fills out and submits their contact form
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse
import urllib.parse

class CompleteBusinessAgent:
    def __init__(self):
        self.session = requests.Session()
        # Set a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_business_website(self, business_name):
        """Search for business website using DuckDuckGo"""
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
                    
        except Exception as e:
            print(f"❌ Search error: {e}")
            
        return None
    
    def is_valid_business_url(self, url, business_name):
        """Check if URL seems to be the business's official website"""
        if not url or url.startswith(('javascript:', 'mailto:')):
            return False
            
        skip_domains = ['google.com', 'facebook.com', 'yelp.com', 'tripadvisor.com', 
                       'opentable.com', 'grubhub.com', 'doordash.com', 'ubereats.com',
                       'duckduckgo.com', 'wikipedia.org']
        
        domain = urlparse(url).netloc.lower()
        for skip in skip_domains:
            if skip in domain:
                return False
                
        return True
    
    def find_contact_form(self, base_url):
        """Find the best contact form on the website"""
        print(f"🔍 Looking for contact forms on: {base_url}")
        
        # First check main page
        try:
            response = self.session.get(base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for contact page links
            contact_links = []
            for link in soup.find_all('a', href=True):
                text = link.get_text().strip().lower()
                href = link['href']
                
                if any(word in text for word in ['contact', 'inquiry', 'get in touch']):
                    contact_url = urljoin(base_url, href)
                    contact_links.append((text, contact_url))
            
            # Check contact pages for forms
            for text, contact_url in contact_links[:2]:  # Check first 2 contact links
                print(f"📞 Checking contact page: {text} -> {contact_url}")
                
                try:
                    contact_response = self.session.get(contact_url, timeout=10)
                    contact_soup = BeautifulSoup(contact_response.text, 'html.parser')
                    
                    # Look for forms on contact page
                    forms = contact_soup.find_all('form')
                    for form in forms:
                        form_info = self.analyze_form(form, contact_url)
                        if form_info and len(form_info['fields']) >= 3:  # Good form
                            print(f"✅ Found suitable contact form!")
                            return form_info, contact_soup
                            
                except Exception as e:
                    print(f"❌ Error checking contact page: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error: {e}")
            
        return None, None
    
    def analyze_form(self, form, form_url):
        """Analyze a form to see if it's suitable for contact"""
        form_info = {
            'url': form_url,
            'method': form.get('method', 'post').lower(),
            'action': form.get('action', ''),
            'fields': [],
            'form_element': form
        }
        
        # Find input fields
        inputs = form.find_all(['input', 'textarea', 'select'])
        
        for inp in inputs:
            field_type = inp.get('type', 'text')
            name = inp.get('name', '')
            placeholder = inp.get('placeholder', '')
            id_attr = inp.get('id', '')
            
            if field_type in ['hidden', 'submit', 'button']:
                continue
                
            field_text = f"{name} {placeholder} {id_attr}".lower()
            
            field_info = {
                'element': inp,
                'type': field_type,
                'name': name,
                'placeholder': placeholder,
                'id': id_attr,
                'tag': inp.name
            }
            
            # Identify field purpose
            if any(word in field_text for word in ['name', 'full', 'first']):
                field_info['purpose'] = 'name'
            elif any(word in field_text for word in ['email', 'mail']):
                field_info['purpose'] = 'email'
            elif any(word in field_text for word in ['phone', 'tel']):
                field_info['purpose'] = 'phone'
            elif any(word in field_text for word in ['message', 'comment', 'inquiry']):
                field_info['purpose'] = 'message'
            else:
                field_info['purpose'] = 'other'
            
            form_info['fields'].append(field_info)
        
        return form_info
    
    def submit_contact_form(self, form_info, soup, form_data):
        """Actually submit the contact form"""
        print(f"📝 Filling out and submitting contact form...")
        
        try:
            # Prepare form data
            post_data = {}
            
            # Add hidden fields
            for hidden in form_info['form_element'].find_all('input', type='hidden'):
                name = hidden.get('name')
                value = hidden.get('value', '')
                if name:
                    post_data[name] = value
                    print(f"🔒 Added hidden field: {name}")
            
            # Fill out visible fields
            filled_count = 0
            for field in form_info['fields']:
                field_name = field['name']
                if not field_name:
                    continue
                    
                if field['purpose'] == 'name':
                    post_data[field_name] = form_data['name']
                    filled_count += 1
                    print(f"✓ Filled name: {form_data['name']}")
                    
                elif field['purpose'] == 'email':
                    post_data[field_name] = form_data['email']
                    filled_count += 1
                    print(f"✓ Filled email: {form_data['email']}")
                    
                elif field['purpose'] == 'phone':
                    post_data[field_name] = form_data['phone']
                    filled_count += 1
                    print(f"✓ Filled phone: {form_data['phone']}")
                    
                elif field['purpose'] == 'message':
                    post_data[field_name] = form_data['message']
                    filled_count += 1
                    print(f"✓ Filled message")
            
            if filled_count == 0:
                print("❌ Could not fill any fields")
                return False
            
            print(f"📝 Filled {filled_count} fields")
            
            # Determine submit URL
            action = form_info['action']
            if action:
                submit_url = urljoin(form_info['url'], action)
            else:
                submit_url = form_info['url']
            
            print(f"🚀 Submitting to: {submit_url}")
            
            # Submit the form
            if form_info['method'] == 'get':
                response = self.session.get(submit_url, params=post_data)
            else:
                response = self.session.post(submit_url, data=post_data)
            
            print(f"📤 Form submitted! Status code: {response.status_code}")
            
            # Check for success indicators
            response_text = response.text.lower()
            success_indicators = [
                'thank you', 'thanks', 'success', 'submitted', 
                'received', 'sent', 'message sent', 'form submitted'
            ]
            
            if any(indicator in response_text for indicator in success_indicators):
                print("🎉 SUCCESS! Form appears to have been submitted successfully!")
                print("📧 The business should receive your message shortly.")
                return True
            else:
                print("⚠️  Form submitted but no clear success message detected.")
                print("📤 The form may have been submitted - check with the business.")
                return True
                
        except Exception as e:
            print(f"❌ Error submitting form: {e}")
            return False
    
    def process_business(self, business_name, form_data):
        """Complete process: search → find form → fill → submit"""
        print(f"\n🎯 Processing: {business_name}")
        print("=" * 50)
        
        # Step 1: Find website
        website = self.search_business_website(business_name)
        if not website:
            print("❌ Could not find business website")
            return False
            
        # Step 2: Find contact form
        form_info, soup = self.find_contact_form(website)
        if not form_info:
            print("❌ Could not find suitable contact form")
            return False
        
        # Step 3: Submit form
        success = self.submit_contact_form(form_info, soup, form_data)
        
        if success:
            print("🎉 Mission accomplished! Form submitted successfully!")
        else:
            print("❌ Failed to submit form")
            
        return success

def main():
    # Form data for Il Pastaio Beverly Hills
    form_data = {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@example.com", 
        "phone": "(555) 987-6543",
        "message": "Hi! I'm interested in making a dinner reservation for 4 people this Saturday evening around 7 PM. Could you please let me know if you have availability? Also, do you have any vegetarian options on your menu? Thank you so much!"
    }
    
    print("🍝 Il Pastaio Beverly Hills Contact Agent")
    print("=" * 50)
    print("📝 Form Data:")
    print(f"   Name: {form_data['name']}")
    print(f"   Email: {form_data['email']}")
    print(f"   Phone: {form_data['phone']}")
    print(f"   Message: {form_data['message'][:100]}...")
    
    agent = CompleteBusinessAgent()
    
    try:
        # Process Il Pastaio Beverly Hills
        success = agent.process_business("Il Pastaio Beverly Hills", form_data)
        
        if success:
            print("\n✅ COMPLETE SUCCESS!")
            print("📧 Your message has been sent to Il Pastaio Beverly Hills!")
            print("🍽️  They should contact you soon for your reservation.")
        else:
            print("\n❌ Could not complete the task")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()