"""
Class for Data Extraction from Dynamo DB Keys
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class DynamoDB(AWSFact):
    """ Class DynamoDB """
    NAME = "DynamoDB"
    OPTION = 'dynamo_keys'

    ORDERED_HEADINGS = [
        'Name',
        'Status',
        'Size',
        'ItemCount',
        'Hash key',
        'Range key'
    ]

    def retrieve(self, conn):

        for table in conn.list_tables()['TableNames']:
            element = conn.describe_table(TableName=table)['Table']
            item = {
                "Name": element['TableName'],
                "Status": element['TableStatus'],
                "Size": element['TableSizeBytes'],
                "ItemCount": element['ItemCount'],
                "Hash key": [el['AttributeName']
                             for el in element['KeySchema'] if el['KeyType'] == 'HASH'][0],
                "Range key": [el['AttributeName']
                              for el in element['KeySchema'] if el['KeyType'] == 'RANGE'][0]
            }
            self.data[conn.region_name].append(item)

    def connect(self, region, aws_key=None):
        conn = boto3.client('dynamodb', region_name=region)
        conn.region_name = region
        return conn
