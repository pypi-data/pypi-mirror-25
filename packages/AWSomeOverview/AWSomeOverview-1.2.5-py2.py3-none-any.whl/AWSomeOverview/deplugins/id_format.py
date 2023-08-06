"""
Class for Data Extraction of IAM
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class IDformat(AWSFact):
    """ Class IDformat """
    NAME = 'IDformat'
    OPTION = 'id_format'

    ORDERED_HEADINGS = ['Resource', 'UseLongIds']

    def retrieve(self, conn):

        account_id = boto3.client('sts').get_caller_identity().get('Account')
        arn = "arn:aws:iam::" + str(account_id) + ":root"
        print('AWS account:', account_id, '   PrincipalArn:', arn,
              '   AWS region:', conn.region_name, '\n')

        data = conn.describe_identity_id_format(PrincipalArn=arn)

        for resource in data['Statuses']:
            item = {
                "Resource": resource['Resource'],
                'UseLongIds': resource['UseLongIds']
            }
            self.data[conn.region_name].append(item)


    def connect(self, region, aws_key=None):
        conn = boto3.client('ec2', region_name=region)
        conn.region_name = region
        return conn
