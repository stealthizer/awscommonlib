#!/usr/bin/env python
from aws.boto_connections import AWSBotoAdapter


class Ec2Adapter:

    def __init__(self, profile):
        self.__connection = AWSBotoAdapter()
        self.__resource = 'ec2'
        self.__profile = profile

    def __get_connection_ec2(self):
        return self.__connection.get_client(self.__resource, self.__profile)

    def get_ec2_instances(self):
        public_ips=[]
        instances = self.__get_connection_ec2().describe_instances()['Reservations']
        for instance in instances:
            print instance.__dict__
            if 'PublicIpAddress' in instance['Instances'][0].keys():
                public_ips.append(instance['Instances'][0]['PublicIpAddress'])
        return public_ips