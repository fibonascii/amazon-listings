import csv
import os
import re
import pandas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


listing_directory = os.path.basename(os.environ["LISTING_DIR"])
listing_file = os.environ["LISTING_FILE"]
listing_output_file = os.environ["LISTING_OUTPUT_FILE"]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


def get_isbn(listing):
    """Grab the ISBN from the listing URL"""
    match = re.search("/([0-9]{0,})/ref", str(listing))
    if match:
        isbn = match.group(1)

        return isbn


def get_amazon_listings():
    """Iterate through listing excel sheet and build a list of all the Listing Links"""
    df = pandas.read_excel(os.path.join(listing_directory, listing_file), header=0, names=["Listings"])
    amazon_listings = df["Listings"].to_list()

    return amazon_listings


def get_listing_prices(amazon_listings):
    """Iterate through the listing list and go to each listing to get the lowest fba price and write to csv"""
    with open(os.path.join(listing_directory, listing_output_file), "w") as output_file:
        header = ["ISBN", "Price"]
        writer = csv.DictWriter(output_file, fieldnames=header)
        writer.writeheader()

        for listing in amazon_listings:
            isbn = get_isbn(listing)
            driver.get(listing)
            try:
                lowest_fba_price = driver.find_element_by_class_name("olpOfferPrice").text
                if isbn and lowest_fba_price:
                    writer.writerow({"ISBN": isbn, "Price": lowest_fba_price})
            except NoSuchElementException:
                pass


if __name__ == '__main__':
    listings = get_amazon_listings()
    get_listing_prices(listings)
