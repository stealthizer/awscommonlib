from aws.ec2_adapter import Ec2Adapter
import troposphere.ec2 as ec2
from troposphere import Ref, Tags

class Ec2SecurityGroupAdapter:

    def __init__(self, connection, region):
        self.ec2op = Ec2Adapter(connection, region)

    def create_security_group(self, template, sg, vpc_id, env):
        security_group_name = sg['security_group_name']
        security_group_name_tag = sg['security_group_name_tag']
        security_group_desc = sg['security_group_desc']
        security_group = template.add_resource(ec2.SecurityGroup(
            security_group_name,
            VpcId=vpc_id,
            GroupDescription=security_group_desc,
            Tags=Tags(
                Name=security_group_name_tag,
                environment=env
            )
        ))
        if 'ingress_rules' in sg:
            self.__create_rules(template, sg['ingress_rules'], security_group, 'ingress')
        elif 'egress_rules' in sg:
            self.__create_rules(template, sg['egress_rules'], security_group, 'egress')
        return security_group

    def __create_rules(self, template, rules, sg, rule_type):
        for rule in rules:
            if rule_type is 'ingress':
                self.__add_ingress_rule(template, rule, sg)
            elif rule_type is 'egress':
                self.__add_egress_rule(template, rule, sg)

    def __add_ingress_rule(self, template, rule, sg):
        if 'sg' in rule:
            template.add_resource(
                ec2.SecurityGroupIngress(
                    rule['name'],
                    ToPort=rule['to_port'],
                    FromPort=rule['from_port'],
                    IpProtocol='tcp',
                    GroupId=Ref(sg),
                    Description=rule['description'],
                    SourceSecurityGroupId=Ref(rule['sg'])
                )
            )
        elif 'cidr_ip' in rule:
            template.add_resource(
                ec2.SecurityGroupIngress(
                    rule['name'],
                    ToPort=rule['to_port'],
                    FromPort=rule['from_port'],
                    IpProtocol='tcp',
                    CidrIp=rule['cidr_ip'],
                    GroupId=Ref(sg),
                    Description=rule['description']
                )
            )
        elif 'instances' in rule:
            count = 0
            instance_ids = self.ec2op.get_instance_ids_from_tag(tag_name="Name", tag_value=rule['instances'])
            for instance_id in instance_ids:
                instance_ip = str(self.ec2op.get_external_ip_from_instance_id(instance_id=instance_id)) + "/32"
                template.add_resource(
                    ec2.SecurityGroupIngress(
                        rule['name'] + str(count),
                        ToPort=rule['to_port'],
                        FromPort=rule['from_port'],
                        IpProtocol='tcp',
                        CidrIp=instance_ip,
                        GroupId=Ref(sg),
                        Description=rule['description']
                    )
                )
                count += 1

    def __add_egress_rule(self, template, rule, sg):
        if 'sg' in rule:
            template.add_resource(
                ec2.SecurityGroupEgress(
                    rule['name'],
                    ToPort=rule['to_port'],
                    FromPort=rule['from_port'],
                    IpProtocol='tcp',
                    GroupId=Ref(sg),
                    Description=rule['description'],
                    DestinationSecurityGroupId=Ref(rule['sg'])
                )
            )
        elif 'cidr_ip' in rule:
            template.add_resource(
                ec2.SecurityGroupEgress(
                    rule['name'],
                    ToPort=rule['to_port'],
                    FromPort=rule['from_port'],
                    IpProtocol='tcp',
                    CidrIp=rule['cidr_ip'],
                    GroupId=Ref(sg),
                    Description=rule['description']
                )
            )

        elif 'instance' in rule:
            count = 0
            instance_ids = self.ec2op.get_instance_ids_from_tag(tag_name="Name", tag_value=rule['instances'])
            for instance_id in instance_ids:
                instance_ip = str(self.ec2op.get_external_ip_from_instance_id(instance_id=instance_id)) + "/32"
                template.add_resource(
                    ec2.SecurityGroupEgress(
                        rule['name'] + str(count),
                        ToPort=rule['to_port'],
                        FromPort=rule['from_port'],
                        IpProtocol='tcp',
                        CidrIp=instance_ip,
                        GroupId=Ref(sg),
                        Description=rule['description']
                    )
                )
                count += 1
