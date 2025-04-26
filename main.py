import os
import requests
import base64
from datetime import datetime, timezone

# Boring tokens and stuff
client_id = os.environ.get("PROD_EBAY_APP_ID")
client_secret = os.environ.get("PROD_EBAY_CERT_ID")
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
token_url = "https://api.ebay.com/identity/v1/oauth2/token"
headers_token = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic " + credentials
}
data = {
    "grant_type": "client_credentials",
    "scope": "https://api.ebay.com/oauth/api_scope"
}
resp_token = requests.post(token_url, headers=headers_token, data=data)
resp_token.raise_for_status()
access_token = resp_token.json().get('access_token', '')

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
    "Authorization": "Bearer " + access_token,
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
