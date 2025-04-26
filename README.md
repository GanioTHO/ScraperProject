# eBay API Search Script

This Python script authenticates with the eBay API using OAuth2, searches for items based on user input (title, offer type, result limit), and saves the results into a JSON file.

It supports:
- OAuth2 authentication flow (with manual code input)
- Saving and refreshing access tokens
- Search functionality with filters (Fixed Price or Auction)
- Saving results into a clean, organized JSON output
- Appending or replacing previous search outputs

---

## Requirements

- Python 3.8+
- An eBay Developer account with API credentials
- Environment variables set:
  - `PROD_EBAY_APP_ID`
  - `PROD_EBAY_CERT_ID`
  - `PROD_EBAY_RUNAME`

Install the required libraries:

```bash
pip install requests
```

---

## Quickstart Example

1. **Set environment variables**:

```bash
export PROD_EBAY_APP_ID=your_app_id
export PROD_EBAY_CERT_ID=your_cert_id
export PROD_EBAY_RUNAME=your_redirect_uri
```

2. **Run the script**:

```bash
cd your/downloaded/file/location
python main.py
```

3. **Authenticate**:  
   - The script opens the eBay login page.
   - Login, allow access, and copy the **full redirect URL** (or extracted `code`).
   - Paste it back into the script when prompted.

4. **Search for products**:  
   - Enter a search keyword (like `laptop`).
   - Specify how many results you want.
   - Choose offer type: `f` (Fixed Price) or `a` (Auction).

5. **Result**:
   - The output will be saved in `output.json`.
   - The file will open automatically when the search finishes.

---

## Notes

- Tokens are stored in `tokens.json` and valid for about **1.5 years**.
- If `tokens.json` is missing or invalid, the script will re-authenticate automatically.
- JSON output structure is optimized for further processing or visualizations.

---

## Author's Comment

> IT WORKS LIKE A F***ING CHARM I LOVE PYTHON 🚀🔥

