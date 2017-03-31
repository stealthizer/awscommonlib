#!/usr/bin/env python
from aws.boto_connections import AWSBotoAdapter

class ElbAdapter:

    def __init__(self, profile):
        self.__connection = AWSBotoAdapter()
        self.__resource = 'elb'
        self.__profile = profile

    def __get_connection_elb(self):
        return self.__connection.get_client(self.__resource, self.__profile)

    def get_elb_ips(self):
        public_dns = []
        elbs = self.__get_connection_elb().describe_load_balancers()['LoadBalancerDescriptions']
        for elb in elbs:
            elb_dict = {}
            if 'internet-facing' in elb['Scheme']:
                elb_dict['public_ip'] = elb['DNSName']
                elb_dict['name'] = elb['LoadBalancerName']
                elb_dict['type'] = "elb"
                public_dns.append(elb_dict)
        return public_dns
