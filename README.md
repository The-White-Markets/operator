# Business Contact Form Automation Agent

A Python agent that automatically finds business websites and fills out their contact forms.

## What it does

Given a business name (like "Il Pastaio Beverly Hills"), this agent will:

1. 🔍 **Search** for the business's official website using Google
2. 📞 **Find** the contact page or reservation form  
3. 📝 **Fill out** the form with your information
4. 🚀 **Submit** the form automatically

## Quick Start

### Prerequisites
- **Python 3.7+** (check with `python3 --version`)
- **Google Chrome** browser installed
- Internet connection

### Installation & Run

1. **Run the setup script:**
   ```bash
   python3 setup_and_run.py
   ```

   This will automatically:
   - Check for Chrome browser
   - Install required Python packages  
   - Run the agent with Il Pastaio Beverly Hills as a test

2. **Watch it work!** 
   - A Chrome browser window will open
   - You'll see it search for the business
   - It will navigate to their website
   - Find and fill out their contact form

### Manual Installation

If you prefer to install manually:

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the agent
python3 business_form_agent.py
```

## How to Use

### Test with Different Businesses

Edit `business_form_agent.py` and change the business name:

```python
# In the main() function, change this line:
success = agent.process_business("Your Business Name Here", form_data)
```

### Customize Form Data

Edit the form data in `business_form_agent.py`:

```python
form_data = {
    "name": "Your Name",
    "email": "your.email@example.com", 
    "phone": "(555) 123-4567",
    "message": "Your custom message here..."
}
```

## Features

- ✅ **Google Search Integration** - Finds business websites automatically
- ✅ **Smart Form Detection** - Identifies contact/reservation forms
- ✅ **Intelligent Field Mapping** - Maps your data to form fields
- ✅ **Auto Chrome Driver** - Downloads Chrome driver automatically
- ✅ **Error Handling** - Robust error handling and retries
- ✅ **Visual Feedback** - See exactly what the agent is doing

## Technical Details

### Dependencies
- `selenium` - Web browser automation
- `beautifulsoup4` - HTML parsing
- `requests` - HTTP requests
- `webdriver-manager` - Automatic Chrome driver management

### How it Works

1. **Search Phase**: Uses Google search to find the business website
2. **Discovery Phase**: Scans the website for contact/reservation pages
3. **Analysis Phase**: Identifies forms and their input fields
4. **Execution Phase**: Fills out and submits the form

### Supported Form Fields

The agent can automatically fill:
- **Name fields** (name, full name, first name)
- **Email fields** (email, e-mail, mail)
- **Phone fields** (phone, telephone, tel)
- **Message fields** (message, comment, inquiry, details)

## Troubleshooting

### Chrome Not Found
```bash
# Install Chrome:
# macOS: Download from https://www.google.com/chrome/
# Linux: sudo apt-get install google-chrome-stable
# Windows: Download from https://www.google.com/chrome/
```

### Permission Errors
```bash
# Try installing with user flag:
pip3 install --user -r requirements.txt
```

### Import Errors
```bash
# Make sure you're using Python 3:
python3 --version
python3 -m pip install -r requirements.txt
```

## Example Output

```
🎯 Processing: Il Pastaio Beverly Hills
==================================================
🔍 Searching for: Il Pastaio Beverly Hills
✅ Found website: https://ilpastaio.com
🔍 Looking for contact page on: https://ilpastaio.com
📞 Found contact page: https://ilpastaio.com/contact
📝 Looking for forms on: https://ilpastaio.com/contact
📋 Found 1 form(s)
🔄 Trying form 1...
✓ Filled name field: John Smith
✓ Filled email field: john.smith@example.com
✓ Filled phone field: (555) 123-4567
✓ Filled message field
📝 Filled 4 fields
🚀 Attempting to submit form...
✅ Successfully filled form!
🎉 Successfully completed form submission!
```

## Safety & Ethics

- This tool is for legitimate business inquiries only
- Always respect robots.txt and website terms of service
- Don't spam businesses with automated messages
- Use reasonable delays between requests
- Test responsibly

## License

MIT License - Feel free to modify and use for your projects!