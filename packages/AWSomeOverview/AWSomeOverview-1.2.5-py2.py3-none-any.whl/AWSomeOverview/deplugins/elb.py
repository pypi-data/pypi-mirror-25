"""
Class for Data Extraction of ELBs
"""

import boto3
from AWSomeOverview.deplugins.base import AWSFact


class ElasticLoadBalancer(AWSFact):
    """ Class ElasticLoadBalancer """
    NAME = "ELB"
    OPTION = 'elb'

    ORDERED_HEADINGS = ['Name', 'ELB-Port', 'ELB-Protocol', 'Instance States', 'ELB-SG']

    def retrieve(self, conn):
        for elb in conn.describe_load_balancers()['LoadBalancerDescriptions']:
            states = {}
            for state in conn.describe_instance_health(
                    LoadBalancerName=elb['LoadBalancerName'])['InstanceStates']:
                states.setdefault(state['State'], []).append(state['InstanceId'])
            state_summary = '; '.join(
                ['%s - %s' % (k, len(v)) for k, v in states.iteritems()])
            item = {
                "Name": elb['LoadBalancerName'],
                "ELB-Port": ','.join(str(i['Listener']['LoadBalancerPort'])
                                     for i in sorted(elb['ListenerDescriptions'])),
                "ELB-Protocol": ','.join(str(i['Listener']['Protocol'])
                                         for i in sorted(elb['ListenerDescriptions'])),
                "Instance States": state_summary,
                "ELB-SG": ','.join(str(i) for i in sorted(elb['SecurityGroups']))
            }

            self.data[conn.region_name].append(item)
        return

    def connect(self, region, aws_key=None):
        conn = boto3.client('elb', region_name=region)
        conn.region_name = region
        return conn
