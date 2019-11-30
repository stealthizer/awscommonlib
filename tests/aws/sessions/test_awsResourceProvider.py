from unittest import TestCase
from moto import mock_iam, mock_sts
from mock import Mock, patch
from aws.sessions.aws_resource_provider import AwsResourceProvider


class TestAwsResourceProvider(TestCase):

    def test_get_resource_by_profile(self):
        credential = 'default'
        region = 'eu-west-1'
        aws_resource = 'ec2'
        session = AwsResourceProvider()

        session.get_resource = Mock()
        resource = session.get_resource(aws_resource, credential, region)
        session.get_resource.assert_called_with(aws_resource, credential, region)


    @mock_iam
    @mock_sts
    def test_get_resource_by_iam(self):
        credential = 'arn:aws:iam::123456789012:role/jenkins'
        region = 'eu-west-1'
        aws_resource = 'ec2'
        session = AwsResourceProvider()

        resource = session.get_resource(aws_resource, credential, region)

        assert('ec2.ServiceResource()' in str(resource))



