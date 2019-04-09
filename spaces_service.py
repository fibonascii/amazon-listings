import boto3
import os
from botocore.client import Config

listing_file = os.environ['INPUT_FILE']


class SpacesService:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client = self.session.client('s3',
                                          region_name='sfo2',
                                          endpoint_url='https://sfo2.digitaloceanspaces.com',
                                          aws_access_key_id="VMLLWHDYIHOVKFMGKY2A",
                                          aws_secret_access_key="74MBUH8ppW2lPyHNPXw5Cj8kZ3vQDblaSWlFBBUYmRY")

    def list_all_buckets(self):
        response = self.client.list_buckets()
        spaces = [space['Name'] for space in response['Buckets']]
        print("Spaces List: {}".format(spaces))

        return spaces

    def download_listing_file(self):
        response = self.client.list_objects(Bucket='amazon-listings-storage')
        for obj in response['Contents']:
            if obj['Key'] == 'listing_files/input_files/{}'.format(listing_file):
                self.client.download_file('amazon-listings-storage',
                                          'listing_files/input_files/{}'.format(listing_file),
                                          '/tmpproject/listing_files/{}'.format(listing_file))

        if os.path.exists('/tmpproject/listing_files/{}'.format(listing_file)):
            return listing_file

    def upload_file(self, output_file):
        response = self.client.upload_file(output_file,
                                           'amazon-listings-storage',
                                           'listing_files/output_files/{}'.format(os.path.basename(output_file)))

        return response