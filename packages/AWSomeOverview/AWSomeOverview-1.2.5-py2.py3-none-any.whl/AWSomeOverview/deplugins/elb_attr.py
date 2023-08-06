"""
Class for Data Extraction of ELBs
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class ElasticLoadBalancer(AWSFact):
    """ Class ElasticLoadBalancer """
    NAME = "ELB Attributes"
    OPTION = 'elb_attr'

    ORDERED_HEADINGS = ['ELB Name', 'ConnectionDraining',
                        'CrossZoneLoadBalancing', 'IdleTimeout', 'AccessLog']

    def retrieve(self, conn):
        for elb in conn.describe_load_balancers()['LoadBalancerDescriptions']:
            attributes = conn.describe_load_balancer_attributes(
                LoadBalancerName=elb['LoadBalancerName'])['LoadBalancerAttributes']
            # import pdb;
            # pdb.set_trace()
            item = {
                "ELB Name": elb['LoadBalancerName'],
                # "ELB Attributes": conn.describe_load_balancer_attributes(
                # LoadBalancerName=lb['LoadBalancerName'])['LoadBalancerAttributes']
                "ConnectionDraining": attributes['ConnectionDraining']['Enabled'],
                "CrossZoneLoadBalancing":   attributes['CrossZoneLoadBalancing']['Enabled'],
                "IdleTimeout": attributes['ConnectionSettings']['IdleTimeout'],
                "AccessLog": attributes['AccessLog']['Enabled'],
            }
            self.data[conn.region_name].append(item)
        return

    def connect(self, region, aws_key=None):
        conn = boto3.client('elb', region_name=region)
        conn.region_name = region
        return conn
