from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import boto3


class AwsResourceProvider:

    AWS_STS = 'sts'

    def __assume_credentials(self, credential, region):
        sts_client = boto3.client(self.AWS_STS, region_name=region)
        assumed_role_object = sts_client.assume_role(
            RoleArn=credential,
            RoleSessionName="Session"
        )
        return assumed_role_object['Credentials']

    def __get_resource_by_profile(self, resource, credential, region):
        aws_connection = boto3.session.Session(region_name=region, profile_name=credential)
        resource = aws_connection.resource(resource, region_name=region)
        return resource

    def __get_resource_by_iam(self, resource, credential, region):
        credentials = self.__assume_credentials(credential, region)
        resource = boto3.resource(
            resource,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=region
        )
        return resource

    def get_resource(self, resource, credential, region):
        if 'arn:' in credential:
            return self.__get_resource_by_iam(resource, credential, region)

        return self.__get_resource_by_profile(resource, credential, region)


