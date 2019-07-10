class Ec2Adapter:

    def __init__(self, connection, region):
        self.__connection = connection
        self.__region = region

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

    def get_latest_ami(self, image):
        filters = [
            {'Name': 'name', 'Values': [image]},
            {'Name': 'tag:Built_from', 'Values': ['master']},
            {'Name': 'root-device-type', 'Values': ['ebs']}
        ]
        return self.__get_newest_image(filters)

    def get_available_subnets(self, vpc_id, filter):
        return self.__get_all_subnets(vpc_id, filter)

    def get_default_vpc(self):
        filters = [
            {'Name': 'isDefault', 'Values': ['true']}
        ]
        return self.__connection.describe_vpcs(Filters=filters)['Vpcs'][0]['VpcId']