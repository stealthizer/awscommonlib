from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase
from mock import patch, Mock
from aws.boto_connections import AWSBotoAdapter


class TestAWSBotoLib(TestCase):

    def test_get_aws_resource(self):
        self.__given_aws_boto_lib()
        self.__given_aws_session()
        self.__when_resource_is_called()
        self.__then_check_if_resource_available()

    def test_get_aws_client_connection(self):
        self.__given_aws_boto_lib()
        self.__given_aws_session()
        self.__when_client_is_called()
        self.__then_check_if_client_available()

    def __given_aws_boto_lib(self):
        self.__aws_boto_lib = AWSBotoAdapter()

    def __given_aws_session(self):
        self.__mocked_aws = Mock()
        self.__mocked_aws.resource = Mock(return_value='resource')
        self.__mocked_aws.client = Mock(return_value='client')

    def __when_resource_is_called(self):
        with patch('boto3.session.Session', return_value=self.__mocked_aws):
            self.__aws_boto_resource = self.__aws_boto_lib.get_resource('aws_resource', 'test')

    def __when_client_is_called(self):
        with patch('boto3.session.Session', return_value=self.__mocked_aws):
            self.__aws_boto_client = self.__aws_boto_lib.get_client('aws_resource', 'test')

    def __then_check_if_resource_available(self):
        self.assertEqual(self.__aws_boto_resource, 'resource')

    def __then_check_if_client_available(self):
        self.assertEqual(self.__aws_boto_client, 'client')
