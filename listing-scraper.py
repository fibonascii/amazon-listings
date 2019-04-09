import csv
import os
import re
import pandas
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from .spaces_service import SpacesService
import datetime

service = SpacesService()

listing_directory = '/tmpproject/listing_files'
listing_output_file = os.path.join(listing_directory, 'listing_output-{}.csv'.format(datetime.datetime.now()))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

print(listing_output_file)


def fetch_input_file():
    input_file = service.download_listing_file()

    return input_file


def get_isbn(listing):
    """Grab the ISBN from the listing URL"""
    match = re.search("/([0-9]*)/ref", str(listing))
    if match:
        isbn = match.group(1)

        return isbn


def get_amazon_listings(input_file):
    """Iterate through listing excel sheet and build a list of all the Listing Links"""
    df = pandas.read_excel(os.path.join(listing_directory, input_file), header=0, names=["Listings"])
    amazon_listings = df["Listings"].to_list()

    return amazon_listings


def get_listing_prices(amazon_listings):
    """Iterate through the listing list and go to each listing to get the lowest fba price and write to csv"""
    with open(listing_output_file, "w") as output_file:
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
                    print("ISBN: {} Price: {}".format(isbn, lowest_fba_price))
            except NoSuchElementException:
                pass


def upload_output_file(listing_output_file):
    service.upload_file(listing_output_file)


if __name__ == '__main__':
    listing_file = fetch_input_file()
    listings = get_amazon_listings(listing_file)
    get_listing_prices(listings)
    upload_output_file(listing_output_file)
