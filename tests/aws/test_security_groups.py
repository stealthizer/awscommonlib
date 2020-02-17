from unittest import TestCase
from anthill.aws.security_groups import Ec2SecurityGroupAdapter
from troposphere import Template
from moto import mock_ec2
import yaml
from cfn_tools import load_yaml, dump_yaml
import boto3


class TestEc2SecurityGroupsAdapter(TestCase):

    def setUp(self):
        self.region = 'eu-west-1'
        self.vpc_id = 'vpc-1234a'
        self.template = Template()
        self.env = "pre"
        self.cidr = "10.10.10.10/32"
        self.sg_name = "TestSecurityGroupName"
        self.instances = "instance*"

    @mock_ec2
    def __given_a_session(self):
        self.ec2_session = boto3.client('ec2', region_name=self.region)
        self.sg = Ec2SecurityGroupAdapter(self.ec2_session, region=self.region)
        self.__mocked_aws = """
        {
            "Reservations": [
                {
                    "Groups": [],
                    "Instances": [
                        {
                            "PublicIpAddress": "52.16.127.187",
                            "InstanceId": "i-00000001",
                            "Tags": [
                                {
                                    "Key": "Name",
                                    "Value": "instance-1"
                                }
                            ],

                        }
                    ]
                },
                {
                    "Groups": [],
                    "Instances": [
                        {
                            "PublicIpAddress": "52.16.127.187",
                            "InstanceId": "i-00000002",
                            "Tags": [
                                {
                                    "Key": "Name",
                                    "Value": "instance-2"
                                }
                            ],

                        }
                    ]
                },
        }
        """

    def __given_a_security_group_with_ingress_cidr_rule(self):
        security_group = """
            security_groups:
              alb_sg:
                security_group_desc: "Allows inbound HTTPS"
                security_group_name: SecurityGroup
                security_group_name_tag: """ + self. env + """-securitygroup
                ingress_rules:
                - cidr_ip: """ + self.cidr + """
                  description: "Test Rule cidr_ip"
                  from_port: 443
                  name: TestRule
                  to_port: 443
            """
        self.mock_security_group = yaml.load(security_group, Loader=yaml.FullLoader)

    def __given_a_security_group_with_ingress_sg_name_rule(self):
        security_group = """
            security_groups:
              instance_sg:
                security_group_desc: "Allows inbound HTTPS"
                security_group_name: SecurityGroup
                security_group_name_tag: """ + self. env + """-securitygroup
                ingress_rules:
                - sg: """ + self.sg_name + """
                  description: "Test Rule sg"
                  from_port: 443
                  name: TestRule
                  to_port: 443
            """
        self.mock_security_group = yaml.load(security_group, Loader=yaml.FullLoader)

    def __given_a_security_group_with_ingress_instance_names(self):
        security_group = """
            security_groups:
              instance_sg:
                security_group_desc: "Allows inbound HTTPS"
                security_group_name: SecurityGroup
                security_group_name_tag: """ + self. env + """-securitygroup
                ingress_rules:
                - instances: """ + self.instances + """
                  description: "Test Rule cidr_ip"
                  from_port: 443
                  name: TestRule
                  to_port: 443
            """
        self.mock_security_group = yaml.load(security_group, Loader=yaml.FullLoader)

    def __given_a_security_group_with_egress_cidr_rule(self):
        security_group = """
            security_groups:
              alb_sg:
                security_group_desc: "Allows inbound HTTPS"
                security_group_name: SecurityGroup
                security_group_name_tag: """ + self. env + """-securitygroup
                egress_rules:
                - cidr_ip: """ + self.cidr + """
                  description: "Test Rule cidr_ip"
                  from_port: 443
                  name: TestRule
                  to_port: 443
            """
        self.mock_security_group = yaml.load(security_group, Loader=yaml.FullLoader)

    def __given_a_security_group_with_egress_sg_name_rule(self):
        security_group = """
            security_groups:
              instance_sg:
                security_group_desc: "Allows inbound HTTPS"
                security_group_name: SecurityGroup
                security_group_name_tag: """ + self. env + """-securitygroup
                egress_rules:
                - sg: """ + self.sg_name + """
                  description: "Test Rule sg"
                  from_port: 443
                  name: TestRule
                  to_port: 443
            """
        self.mock_security_group = yaml.load(security_group, Loader=yaml.FullLoader)

    def __when_a_security_group_is_created_to_use_cidr(self):
        self.sg.create_security_group(template=self.template,
                                      sg=self.mock_security_group['security_groups']['alb_sg'],
                                      vpc_id=self.vpc_id, env=self.env)

    def __when_a_security_group_is_created_to_use_sg_name(self):
        self.sg.create_security_group(template=self.template,
                                      sg=self.mock_security_group['security_groups']['instance_sg'],
                                      vpc_id=self.vpc_id, env=self.env)

    def __when_a_security_group_is_created_to_use_instances(self):
        self.sg.create_security_group(template=self.template,
                                      sg=self.mock_security_group['security_groups']['instance_sg'],
                                      vpc_id=self.vpc_id, env=self.env)

    def test_should_return_security_group_with_ingress_cidr_rule(self):
        self.__given_a_session()
        self.__given_a_security_group_with_ingress_cidr_rule()
        self.__when_a_security_group_is_created_to_use_cidr()
        result = yaml.load(dump_yaml(load_yaml(self.template.to_yaml())), Loader=yaml.FullLoader)
        self.assertEqual(result['Resources']['TestRule']['Properties']['CidrIp'], self.cidr)

    def test_should_return_security_group_with_ingress_sg_name_rule(self):
        self.__given_a_session()
        self.__given_a_security_group_with_ingress_sg_name_rule()
        self.__when_a_security_group_is_created_to_use_sg_name()
        result = yaml.load(dump_yaml(load_yaml(self.template.to_yaml())), Loader=yaml.FullLoader)
        self.assertEqual(result['Resources']['TestRule']['Properties']['SourceSecurityGroupId']['Ref'], self.sg_name)

    def test_should_return_security_group_with_egress_cidr_rule(self):
        self.__given_a_session()
        self.__given_a_security_group_with_egress_cidr_rule()
        self.__when_a_security_group_is_created_to_use_cidr()
        result = yaml.load(dump_yaml(load_yaml(self.template.to_yaml())), Loader=yaml.FullLoader)
        self.assertEqual(result['Resources']['TestRule']['Properties']['CidrIp'], self.cidr)

    def test_should_return_security_group_with_egress_sg_name_rule(self):
        self.__given_a_session()
        self.__given_a_security_group_with_egress_sg_name_rule()
        self.__when_a_security_group_is_created_to_use_sg_name()
        result = yaml.load(dump_yaml(load_yaml(self.template.to_yaml())), Loader=yaml.FullLoader)
        self.assertEqual(result['Resources']['TestRule']['Properties']['DestinationSecurityGroupId']['Ref'],
                         self.sg_name)
'''
    def test_should_return_security_group_with_ingress_instance_ips(self):
        self.__given_a_session()
        self.__given_a_security_group_with_ingress_instance_names()
        self.__when_a_security_group_is_created_to_use_instances()
        result = yaml.load(dump_yaml(load_yaml(self.template.to_yaml())))
        print(result)
        exit(1)
        self.assertEqual(result['Resources']['TestRule']['Properties']['CidrIp'], self.cidr)
'''