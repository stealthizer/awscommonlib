from unittest import TestCase
from moto import mock_iam, mock_sts


from awscommonlib.aws.sessions.aws_client_provider import AwsClientProvider



class TestAwsClientProvider(TestCase):


    def test_get_client_by_profile(self):
        credential = 'milanuncios-pre'
        region = 'eu-west-3'
        aws_resource = 'ec2'
        session = AwsClientProvider()

        client = session.get_client(aws_resource, credential, region)

        assert('botocore.client.EC2' in str(client))



    @mock_iam
    @mock_sts
    def test_get_client_by_iam(self):
        credential = 'arn:aws:iam::123456789012:role/jenkins'
        region = 'eu-west-3'
        aws_resource = 'ec2'
        session = AwsClientProvider()

        client = session.get_client(aws_resource, credential, region)

        assert('botocore.client.EC2' in str(client))

