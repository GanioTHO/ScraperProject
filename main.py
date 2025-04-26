import os
import requests
from datetime import datetime, timezone
import json
import webbrowser
from urllib.parse import unquote

# IT WORKS LIKE A FUCKING CHARM I LOVE PYTHON

def authentication(file_path="tokens.json"):
    # Step 1: OAuth Authorization URL
    client_id = "PROD_EBAY_APP_ID"
    redirect_uri = "PROD_EBAY_RUNAME"
    scope = "https://api.ebay.com/oauth/api_scope"

    auth_url = (
        "https://auth.ebay.com/oauth2/authorize?"
        f"client_id={client_id}&"
        "response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}"
    )

    # Open the OAuth URL in the default web browser
    webbrowser.open(auth_url)
    print("----------------------------------------------------------------------------------------------------------")
    print("WARNING! MAKE SURE TO COPY URL AFTER LOGGING IN. WEBSITE WILL TELL YOU TO CLOSE BROWSER TAB. DON'T DO IT!")
    print("----------------------------------------------------------------------------------------------------------")
    print("The OAuth signup page has been opened in your default web browser.")

    # Step 2: Get Authorization Code from User
    def get_auth_code():
        # Wait for the user to press Enter after completing authorization
        input("After completing the OAuth process, press Enter to continue...")

        # Prompt user to paste the full redirect URI or extracted authorization code
        full_url = input(
            "Paste the full redirect URL you were redirected to here: "
        ).strip()

        # If they paste the full URL, extract the `code` query parameter
        if "code=" in full_url:
            auth_code = full_url.split("code=")[1].split("&")[0]
            auth_code = unquote(auth_code)  # URL-decode the authorization code
            return auth_code
        else:
            # Assume user directly pastes the authorization code and decode it just in case
            return unquote(full_url)

    # Step 3: Exchange Authorization Code for Tokens
    def fetch_tokens(auth_code):
        import base64

        token_url = "https://api.ebay.com/identity/v1/oauth2/token"
        client_id = "PROD_EBAY_APP_ID"  # Replace with your actual client_id
        client_secret = "PROD_EBAY_CERT_ID"  # Replace with your actual client_secret
        redirect_uri = "PROD_EBAY_RUNAME"  # Replace with your registered redirect URI

        # Base64 encode the client credentials
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        # Request headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_base64}",
        }

        # POST body
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,  # Use the decoded authorization code
            "redirect_uri": redirect_uri,  # Be sure this matches your eBay app settings
        }

        # Make the POST request
        response = requests.post(token_url, headers=headers, data=data)
        return response.json()

    def save_tokens(tokens, file_path="tokens.json"):
        with open(file_path, "w") as file:
            json.dump(tokens, file, indent=4)
        print(f"Tokens successfully saved to {file_path}.")
        print("You can use the app for 1,5 years. After that time you will be required to re-authorize the app. Ebay thing duh")

    # Integrated Workflow
    auth_code = get_auth_code()  # Fetch the authorization code manually
    if auth_code:
        print(f"Authorization code received! Proceeding...")
        tokens = fetch_tokens(auth_code)  # Exchange the code for tokens
        if "access_token" in tokens:
            save_tokens(tokens)  # Save tokens to tokens.json
    else:
        print("No authorization code provided.")

# Boring tokens and stuff
def load_access_token(file_path="tokens.json"):
    try:
        with open(file_path, "r") as file:
            tokens = json.load(file)
            return tokens["access_token"]
    except(FileNotFoundError, json.decoder.JSONDecodeError):
        print("No tokens found. Please authenticate first.")
        authentication()
        return load_access_token(file_path=file_path)

access_token = load_access_token()

# Filters and search engine
search_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
title = input("What do you want to search for? ")
limit = input("How many results do you want? ")
offer_type = ''
while offer_type != 'f' and offer_type != 'a':
    offer_type = input("What offer type do you want? Type 'f' for FIXED_PRICE or 'a' for AUCTION: ").lower()
    if offer_type != 'f' and offer_type != 'a':
        print("Invalid input! 'f' for FIXED_PRICE or 'a' for AUCTION: ")
offer_type = offer_type.replace(" ", "_")
offer_type = offer_type.replace("a", "AUCTION")
offer_type = offer_type.replace("f", "FIXED_PRICE")

output_file = "output.txt"
is_file_empty = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

want_to_append = ''
while want_to_append != 'a' and want_to_append != 'r':
    want_to_append = input("Do you want to append or replace the output file? Type 'a' for append and 'r' for replace: ").strip().lower()
    if want_to_append != 'a' and want_to_append != 'r':
        print("Invalid input! 'a' for append and 'r' for replace: ")

if is_file_empty:
    # Output file is empty or doesn't exist. Using replace mode to not add spaces at the begining of the file
    file_mode = 'w'
else:
    if want_to_append == 'a':
        file_mode = 'a'
        with open(output_file, file_mode) as file:
            file.write("\n\n\n")
    else:
        file_mode = 'w'

print("Searching...")

params = {
    "q": f"{title}",
    "limit": limit,
#TODO 1: Add price filter
    "filter": f"buyingOptions:{{{offer_type}}}"
}
headers_search = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
resp_search = requests.get(search_url, headers=headers_search, params=params)
resp_search.raise_for_status()
data = resp_search.json()

# Write to file based on determined mode
with open(output_file, file_mode) as file:
    file.write(f"Data for {title}, limit {limit}, offer type {offer_type}, time of scraping: {str(datetime.now())[:-7]}")
    file.write("\n\n\n")
    for item in data.get('itemSummaries', []):
        file.write(item['title'] + "\n")
        if offer_type == "FIXED_PRICE":
            file.write(f"Price: {item['price']['value']} {item['price']['currency']}\n")
        elif offer_type == "AUCTION":
            file.write("Current bid price is: " + item['currentBidPrice']['value'] + " " + item['currentBidPrice']['currency'] + "\n")
            end_str = item['itemEndDate']
            end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            until_end = end - now
            file.write("Bid ends in: " + str(until_end)[:-7] + "\n")
        file.write(item.get('itemWebUrl', 'No link available') + "\n")
        file.write("\n")

print("Done! Opening file...")
os.startfile(output_file)


