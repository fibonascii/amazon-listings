import pandas
import os
import re
import csv


listing_directory = os.path.basename("listing_files")


def get_list_of_isbns():
    df = pandas.read_excel(os.path.join(listing_directory, "Isbns.xlsx"), header=0, names=["Isbns"])
    isbn_list = df["Isbns"].to_list()

    return isbn_list


def format_amazon_links(isbn_list):

    df = pandas.read_excel(os.path.join(listing_directory, "Listings.xlsx"), header=0, names=["Listings"])
    amazon_listings = df["Listings"].to_list()

    with open("listing_files/NewListings.csv", "w") as output_file:
        header = ["Listing"]
        writer = csv.DictWriter(output_file, fieldnames=header)
        for listing, isbn in zip(amazon_listings, isbn_list):
            updated_isbn = re.sub("/([0-9]{0,})/ref", "/{}/ref".format(isbn), str(listing))
            writer.writerow({"Listing": updated_isbn})


if __name__ == "__main__":
    isbn_list = get_list_of_isbns()
    format_amazon_links(isbn_list)
