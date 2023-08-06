"""
Class for Data Extraction of S3
"""

import boto3

from AWSomeOverview.deplugins.base import AWSFact


class S3Buckets(AWSFact):
    """ Class S3Buckets """
    NAME = 'S3'
    OPTION = 's3'

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        for bucket in boto3.resource('s3').buckets.all():
            item = {"Name": bucket.name, 'Created': bucket.creation_date}
            self.data.setdefault('N/A', []).append(item)

    def connect(self, region, aws_key=None):
        return
