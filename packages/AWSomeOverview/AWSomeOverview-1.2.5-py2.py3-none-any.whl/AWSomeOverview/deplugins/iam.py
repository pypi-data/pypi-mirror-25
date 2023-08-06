"""
Class for Data Extraction of IAM
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class IAMusers(AWSFact):
    """ Class IAMusers """
    NAME = 'IAM'
    OPTION = 'iam'

    ORDERED_HEADINGS = ['Name', 'ARN']

    def get_all_regions(self):
        return [None]

    def retrieve(self, conn):
        if conn.get_role(RoleName='syseng'):
            print('\n++++++++++++++++++++++++++++++++++++++++++++\nSupport role "syseng" found!')
            if conn.get_role_policy(RoleName='syseng', PolicyName='syseng-full-access-policy'):
                print('Policy "syseng-full-access-policy" for Syseng role also found!' +
                      '\n++++++++++++++++++++++++++++++++++++++++++++\n')

        data = conn.list_users()['Users']
        for user in data:
            item = {
                "Name": user['UserName'],
                'Arn': user['Arn']
            }
            self.data.setdefault('N/A', []).append(item)

    def connect(self, region, aws_key=None):
        conn = boto3.client('iam')

        return conn
