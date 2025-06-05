import urllib.parse
from olx import OlxScraper
from ebay import EbayScraper

def run_olx_flow():
    search = input("What do you want to search for on OLX? ").strip()
    min_price = input("Provide minimum price [PLN] (or leave empty): ").strip()
    min_price = int(min_price) if min_price.isdigit() else 0
    max_price = input("Provide maximum price [PLN] (or leave empty): ").strip()
    max_price = int(max_price) if max_price.isdigit() else 0
    num_results = input("How many OLX results do you want to save? Leave empty for all: ").strip()
    num_results = int(num_results) if num_results.isdigit() else None
    print("Note: OLX results will be scraped by lowest price first.")
    output_file = input("Specify OLX output file name (will overwrite if exists): ").strip()

    encoded_search = urllib.parse.quote(search)
    base_url = f"https://www.olx.pl/oferty/q-{encoded_search}/"

    scraper = OlxScraper(
        url=base_url,
        min_price=min_price,
        max_price=max_price,
        output_filename=output_file,
        search_term="",
    )

    offers = scraper.get_offers()

    if offers:
        scraper.save_to_file(offers, limit=num_results)
        print(f"Saved OLX offers to Output/OLX/{output_file}")
    else:
        print("No OLX offers found for provided criteria.")

def run_ebay_flow():
    print("This part uses eBay API and requires valid API keys.")

    # Instantiate once to ensure token check/authentication happens before prompts
    scraper = EbayScraper(
        search_title="",  # Will update later
        limit=None,
        min_price="",
        max_price="",
        offer_type="f",
        output_file="",
        pre_auth_check=True  # NEW ARG TO CONTROL TOKEN CHECK
    )

    title = input("What do you want to search for on eBay? ").strip()
    min_price = input("Provide minimum price [USD] (or leave empty): ").strip()
    max_price = input("Provide maximum price [USD] (or leave empty): ").strip()
    limit = input("How many eBay results do you want? Leave empty for all: ").strip()
    limit = int(limit) if limit.isdigit() else None

    offer_type = ''
    while offer_type not in ('f', 'a'):
        offer_type = input("What offer type do you want? Type 'f' for FIXED_PRICE or 'a' for AUCTION: ").lower()

    output_file = input("Specify eBay output filename (will overwrite if exists): ").strip()

    # Reinitialize with full values now
    scraper = EbayScraper(
        search_title=title,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        offer_type=offer_type,
        output_file=output_file
    )
    scraper.run()

def main():
    print("Choose platform to scrape:")
    print("1 - OLX (no API key needed)")
    print("2 - eBay (API keys required)")
    print("3 - Both (runs OLX and eBay sequentially)")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        run_olx_flow()
    elif choice == "2":
        run_ebay_flow()
    elif choice == "3":
        print("Running OLX scraper first:")
        run_olx_flow()
        print("\nRunning eBay scraper next:")
        run_ebay_flow()
    else:
        print("Invalid choice. Exiting.")

main()
