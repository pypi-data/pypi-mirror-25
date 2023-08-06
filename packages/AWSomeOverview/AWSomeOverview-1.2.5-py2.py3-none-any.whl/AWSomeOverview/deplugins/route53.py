"""
Class for Data Extraction of Route 53
"""

from copy import copy

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class Route53(AWSFact):
    """ Class Route53 """
    NAME = 'Route53'
    OPTION = 'r53'

    ORDERED_HEADINGS = [
        'Zone', 'Name', 'Type']#, 'TTL', 'Record', 'Identifier', 'Region']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        for zone in conn.list_hosted_zones_by_name()['HostedZones']:
            base_item = {'Zone': zone['Name']}
            for rec in conn.list_resource_record_sets(HostedZoneId=zone['Id'])['ResourceRecordSets']:
                mid_item = copy(base_item)
                mid_item['Name'] = rec['Name']
                mid_item['Type'] = rec['Type']

            self.data.setdefault(None, []).append(mid_item)

    def connect(self, region, aws_key=None):
        conn = boto3.client('route53')

        return conn
