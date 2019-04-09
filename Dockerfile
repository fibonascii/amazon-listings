FROM selenium/standalone-chrome

RUN sudo apt-get update -y
RUN sudo apt-get install -y python3-dev python3-pip
RUN pip3 install xlrd pandas selenium boto3

RUN sudo mkdir /tmpproject
RUN sudo mkdir /tmpproject/listing_files
RUN sudo chown -R seluser:seluser /tmpproject

WORKDIR /tmpproject
#ADD listing_files/NewListings.xls /tmpproject/listing_files
COPY listing_files/ /tmpproject/listing_files/
ADD listing-scraper.py /tmpproject/
ADD spaces_service.py /tmpproject/

CMD ["python3", "-u", "/tmpproject/listing-scraper.py"]