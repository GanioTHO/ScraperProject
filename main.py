import requests
from datetime import datetime, timezone
import json
import webbrowser
from urllib.parse import unquote
import os

# Boring tokens and stuff
def authentication(file_path="tokens.json"):
    # OAuth authorization
    client_id = os.environ.get("PROD_EBAY_APP_ID")
    redirect_uri = os.environ.get("PROD_EBAY_RUNAME")
    scope = "https://api.ebay.com/oauth/api_scope"

    auth_url = (
        "https://auth.ebay.com/oauth2/authorize?"
        f"client_id={client_id}&"
        "response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}"
    )

    # Open auth window in browser
    webbrowser.open(auth_url)
    print("----------------------------------------------------------------------------------------------------------")
    print("WARNING! MAKE SURE TO COPY URL AFTER LOGGING IN. WEBSITE WILL TELL YOU TO CLOSE BROWSER TAB. DON'T DO IT!")
    print("----------------------------------------------------------------------------------------------------------")
    print("The OAuth signup page has been opened in your default web browser.")

    # Prompts user to provide link
    def get_auth_code():
        input("After completing the OAuth process, press Enter to continue...")

        full_url = input(
            "Paste the full redirect URL you were redirected to here: "
        ).strip()

        if "code=" in full_url:
            auth_code = full_url.split("code=")[1].split("&")[0]
            auth_code = unquote(auth_code)
            return auth_code
        else:
            return unquote(full_url)

    # Authorization
    def fetch_tokens(auth_code):
        import base64

        token_url = "https://api.ebay.com/identity/v1/oauth2/token"
        client_id = os.environ.get("PROD_EBAY_APP_ID")
        client_secret = os.environ.get("PROD_EBAY_CERT_ID")
        redirect_uri = os.environ.get("PROD_EBAY_RUNAME")

        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_base64}",
        }

        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(token_url, headers=headers, data=data)
        return response.json()

    # Saves tokens to tokens.json
    def save_tokens(tokens, file_path="tokens.json"):
        with open(file_path, "w") as file:
            json.dump(tokens, file, indent=4)
        print(f"Tokens successfully saved to {file_path}.")
        print("You can use the app for 1,5 years. After that time you will be required to re-authorize the app. Ebay thing duh")

    auth_code = get_auth_code()
    if auth_code:
        print(f"Authorization code received! Proceeding...")
        tokens = fetch_tokens(auth_code)
        if "access_token" in tokens:
            save_tokens(tokens)
    else:
        print("No authorization code provided.")

# Load token if generated
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

output_file = "output.json"
is_file_empty = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

want_to_append = ''
while want_to_append != 'a' and want_to_append != 'r':
    want_to_append = input("Do you want to append or replace the output file? Type 'a' for append and 'r' for replace: ").strip().lower()
    if want_to_append != 'a' and want_to_append != 'r':
        print("Invalid input! 'a' for append and 'r' for replace: ")

if is_file_empty or want_to_append == 'r':
    mode = "replace"
else:
    mode = "append"

print("Searching...")

params = {
    "q": f"{title}",
    "limit": limit,
    # TODO: Add price filter
    "filter": f"buyingOptions:{{{offer_type}}}"
}
headers_search = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
resp_search = requests.get(search_url, headers=headers_search, params=params)
resp_search.raise_for_status()
data = resp_search.json()

results = []
for item in data.get('itemSummaries', []):
    item_data = {
        "title": item['title'],
        "url": item.get('itemWebUrl', 'No link D:')
    }
    if offer_type == "FIXED_PRICE":
        item_data["price"] = {
            "value": item['price']['value'],
            "currency": item['price']['currency']
        }
    elif offer_type == "AUCTION":
        item_data["current_bid_price"] = {
            "value": item['currentBidPrice']['value'],
            "currency": item['currentBidPrice']['currency']
        }
        end_str = item['itemEndDate']
        end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        until_end = end - now
        item_data["bid_ends_in"] = str(until_end)[:-7]
    results.append(item_data)

output_data = {
    "metadata": {
        "search_title": title,
        "result_limit": limit,
        "offer_type": offer_type,
        "scraped_at": str(datetime.now())[:-7]
    },
    "items": results
}

if mode == "append" and os.path.exists(output_file):
    with open(output_file, "r") as file:
        existing_data = json.load(file)
    existing_data["items"].append({"metadata": output_data["metadata"]})
    existing_data["items"].extend(output_data["items"])
    output_data = existing_data

with open(output_file, "w") as file:
    json.dump(output_data, file, indent=4)

print("Done! Opening file...")
os.startfile(output_file)
