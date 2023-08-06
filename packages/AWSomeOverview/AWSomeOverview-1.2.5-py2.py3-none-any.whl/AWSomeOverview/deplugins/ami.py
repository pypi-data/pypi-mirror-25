"""
Class for Data Extraction of AMIs
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class AMI(AWSFact):
    """ Class AMI """
    NAME = "AMI"
    OPTION = 'ami'
    ORDERED_HEADINGS = ['ID', 'RootDeviceType', 'DeleteOnTerm',
                        'DeviceName', 'Name', 'Description']

    def retrieve(self, conn):
        for element in conn.describe_images(DryRun=False, Owners=['self'])['Images']:

            item = {
                "Name": element['Name'],
                'ID': element['ImageId'],
                'Description': element.get('Description',),
                'DeviceName': ','.join(str(i['DeviceName'])
                                       for i in sorted(element['BlockDeviceMappings'])),
                'RootDeviceType': element['RootDeviceType'],
                'DeleteOnTerm': ','.join(str(i.get('Ebs', {}).get('DeleteOnTermination', 'N/A'))
                                         for i in sorted(element['BlockDeviceMappings'])),
            }
            self.data[conn.region_name].append(item)

    def connect(self, region, aws_key=None):
        conn = boto3.client('ec2', region_name=region)
        conn.region_name = region
        return conn
