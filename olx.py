import requests
from bs4 import BeautifulSoup
import os


class OlxScraper:
    def __init__(self, url, min_price=0, max_price=0, output_filename="output.txt", search_term=""):
        self.url = url
        self.min_price = min_price
        self.max_price = max_price
        self.output_filename = output_filename
        self.search_term = search_term

    def get_offers(self):
        params = {}

        # Price filters for OLX URL parameters
        if self.min_price:
            params["search[filter_float_price:from]"] = str(self.min_price)
        if self.max_price:
            params["search[filter_float_price:to]"] = str(self.max_price)

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(self.url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        offers = []

        for offer in soup.find_all("div", attrs={"data-cy": "l-card"}):
            title_tag = offer.find("h4", class_="css-1g61gc2")
            link_tag = offer.find("a", href=True)
            price_tag = offer.find("p", class_="css-uj7mm0")

            if title_tag and link_tag and price_tag:
                title = title_tag.text.strip()
                price = price_tag.text.strip()
                link = "https://www.olx.pl" + link_tag["href"]

                # Filter by search_term inside title
                if self.search_term.lower() in title.lower():
                    offers.append((price, title, link))

        return offers

    def save_to_file(self, offers, limit=None):
        valid_offers = []
        for offer in offers:
            try:
                price = offer[0].replace(' zł', '').replace(' ', '').replace(',', '.')
                price_value = float(price)
                valid_offers.append((price_value, offer[1], offer[2]))
            except ValueError:
                continue

        valid_offers.sort(key=lambda x: x[0])

        if limit is not None:
            valid_offers = valid_offers[:limit]

        os.makedirs("Output/OLX", exist_ok=True)
        output_path = os.path.join("Output/OLX", self.output_filename)

        with open(output_path, "w", encoding="utf-8") as file:
            for price, title, link in valid_offers:
                file.write(f"{price} zł | {title} | {link}\n")
