# eBay & OLX Scraper CLI Tool

A powerful Python CLI tool that searches and saves listings from:

- **OLX.pl** (no API keys required)
- **eBay** (API keys required)
- Or both (dual search + output)

Supports filters like min/max price, listing type (auction/fixed), and result limits.

---

## 🚀 Features

- ✅ eBay OAuth2 authentication with token caching (1.5 years valid)
- ✅ OLX web scraping (sorted by lowest price)
- ✅ CLI-based input for flexible one-time use
- ✅ Automatically saves results into:
  - `Output/OLX/filename.txt`
  - `Output/EBAY/filename.txt`
- ✅ Option to run either or both scrapers

---

## 📦 Requirements

- Python 3.8+
- `requests`, `bs4` libraries (install below)
- For eBay:
  - An **eBay Developer Account**
  - Valid App ID, Cert ID, and Redirect URI (RUNAME)

Install dependencies:

```bash
pip install requests beautifulsoup4
````
---
## ⚙️ eBay API Authentication Setup
You can choose between environment variables or hardcoding credentials directly into the code. 
## ✅ Option 1: Environment Variables (Recommended)

Set your credentials in your terminal:
Linux/macOS:
````
export PROD_EBAY_APP_ID=your_app_id
export PROD_EBAY_CERT_ID=your_cert_id
export PROD_EBAY_RUNAME=your_redirect_uri
````
Windows (CMD):
````
set PROD_EBAY_APP_ID=your_app_id
set PROD_EBAY_CERT_ID=your_cert_id
set PROD_EBAY_RUNAME=your_redirect_uri
````
The script will automatically read from these environment variables if set.


## ✅ Option 2: Hardcode in Code (Fallback if env vars are missing)

If you prefer not to use environment variables:

1. Open ````ebay.py````

2. In the authentication() function (lines 32-34) insert your credentials:

````
# HARDCODED EBAY API CREDENTIALS (used if env vars are not set)
EBAY_APP_ID = "your_app_id_here"
EBAY_CERT_ID = "your_cert_id_here"
EBAY_RUNAME = "your_redirect_uri_here"
````
⚠️ The script will fallback to these values if no environment variables are set.

🔒 Important: Never commit your credentials to version control (e.g., GitHub).



---
## 🧪 Usage

1. Run the main script:
````
    python main.py
````

2. Choose platform:
 - 1 for OLX (no API keys needed)
 - 2 for eBay (API keys required)
 - 3 for both (runs OLX scraper, then eBay scraper)

3. Follow prompts for your search criteria:
- Search keywords
- Min/max price filters (optional)
- Number of results to save (optional)
- Output filename (existing files will be overwritten)
  - For eBay, choose offer type:
    - f for Fixed Price
    - a for Auction
    - 
4. Authentication (eBay only):
- The script opens your default browser for OAuth login.
- Login, allow access, copy the full redirect URL you are redirected to.
- Paste that URL back into the script when prompted.
- Tokens are saved in tokens.json and reused until expiration.

---

## 📤 Output

- OLX results are saved in Output/OLX/{your_filename}.
- eBay results are saved in Output/EBAY/{your_filename}.
- Each file contains results in the format:
````
price currency | title | url
````
- Results are sorted by price (lowest first for OLX).

---

## 📝 Notes

- OLX scraping relies on HTML structure, so changes on OLX website might break it.

- eBay API results require valid tokens and network access.

- Tokens last approx 1.5 years before needing re-authentication.

--- 

## 🛠️ Troubleshooting

- If you get authentication errors with eBay, delete tokens.json and re-run the script to re-authenticate.
- Make sure your environment variables are correctly set and match your eBay app credentials.
- For OLX, if no results show, double-check your search term and price filters.
- If you can't set your env variables with CLI, use GUI
- I strongly suggest using env variables.
- ---
ENJOY :)