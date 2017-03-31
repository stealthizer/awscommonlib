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
        public_ips = []
        instances = self.__get_connection_ec2().describe_instances()['Reservations']
        for instance in instances:
            if 'PublicIpAddress' in instance['Instances'][0].keys():
                instance_dict = {}
                instance_dict['public_ip'] = instance['Instances'][0]['PublicIpAddress']
                instance_dict['type'] = "instance"
                if 'Tags' in instance['Instances'][0]:
                    for tags in instance['Instances'][0]['Tags']:
                        for key in tags.keys():
                            if key == 'Key':
                                if tags['Key'] == 'Name':
                                    instance_dict['name'] = tags['Value']
                    public_ips.append(instance_dict)
        return public_ips

