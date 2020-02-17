#!/usr/bin/env python
from aws.boto_connections import AWSBotoAdapter


class Ec2Adapter:

    def __init__(self, connection, region):
        self.__connection = connection
        self.__region = region

    def __get_ami_list(self, filters):
        return self.__connection.describe_images(Filters=filters)

    def __get_newest_image(self, filters):
        response = self.__get_ami_list(filters)
        amis = sorted(
            response['Images'],
            key=lambda x: x['CreationDate'],
            reverse=True
        )
        return amis[0]['ImageId']

    def __get_all_subnets(self, vpcId, filter):
        filters = [
            {'Name': 'vpc-id', 'Values': [vpcId]},
            {'Name': 'tag:Name', 'Values': [filter]}
        ]
        subnets = []
        all_subnets = self.__connection.describe_subnets(Filters=filters)['Subnets']
        for subnet in all_subnets:
            subnets.append(subnet['SubnetId'])
        return subnets

    def get_latest_ami(self, image):
        filters = [
            {'Name': 'name', 'Values': [image]},
            {'Name': 'tag:Built_from', 'Values': ['master']},
            {'Name': 'root-device-type', 'Values': ['ebs']}
        ]
        return self.__get_newest_image(filters)

    def get_available_subnets(self, vpcId, filter):
        return self.__get_all_subnets(vpcId, filter)

    def get_default_vpc(self):
        filters = [
            {'Name': 'isDefault', 'Values': ['true']}
        ]
        return self.__connection.describe_vpcs(Filters=filters)['Vpcs'][0]['VpcId']

    def get_security_group_from_name(self, security_group_name):
        filters = [
            {'Name': 'group-name', 'Values': [security_group_name]}
        ]
        return self.__connection.describe_security_groups(Filters=filters)['SecurityGroups'][0]['GroupId']

    def get_external_ip_from_instance_id(self, instance_id):
        filters = [
            {'Name': 'instance-id', 'Values': [instance_id]}
        ]

        return self.__connection.describe_instances(Filters=filters)['Reservations'][0]['Instances'][0]['PublicIpAddress']

    def get_instance_ids_from_tag(self, tag_value, tag_name='Name'):
        filters = [
            {'Name': 'tag:' + tag_name, 'Values': [tag_value]}
        ]

        instance_ids = list()
        for reservation in self.__connection.describe_instances(Filters=filters)['Reservations']:
            instance_ids.append(reservation['Instances'][0]['InstanceId'])

        return instance_ids


