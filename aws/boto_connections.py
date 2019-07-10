import boto3


class AWSBotoAdapter(object):

    AWS_REGION = 'eu-west-1'

    def get_resource(self, resource, profile):
        aws_connection = boto3.session.Session(region_name=self.AWS_REGION, profile_name=profile)
        resource = aws_connection.resource(resource, region_name=self.AWS_REGION)
        return resource

    def get_client(self, client, profile):
        aws_connection = boto3.session.Session(region_name=self.AWS_REGION, profile_name=profile)
        client = aws_connection.client(client, region_name=self.AWS_REGION)
        return client
