"""
Class for Data Extraction from CloudFront
"""

import boto3

from AWSomeOverview.deplugins.base import AWSFact


class CloudFront(AWSFact):
    """ Class CloudFront Aliases """
    NAME = "CloudFront-Aliases"
    OPTION = 'cfront_aliases'

    ORDERED_HEADINGS = ['Id', 'Status', 'Aliases']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        for element in conn.list_distributions().get('DistributionList', {}).get('Items', []):
            item = {
                "Id": element['Id'],
                "Aliases": element['Aliases']['Items'],
                "Status": element['Status'],
            }
            self.data.setdefault('N/A', []).append(item)

    def connect(self, region, aws_key=None):
        conn = boto3.client('cloudfront', region_name=region)
        conn.region_name = region
        return conn
