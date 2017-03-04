#!/usr/bin/env python
from aws.boto_connections import AWSBotoAdapter


class Cloudformation(object):

    def __init__(self, profile, resource, name):
        self.__profile = profile
        self.__connection = AWSBotoAdapter()
        self.__resource = resource
        self.__name = name
        self.__stackName = self.__name

    def get_stackName(self):
        return self.__stackName

    def get_connection_cloudformation(self):
        conn = self.__connection.get_client(self.__resource, self.__profile)
        return conn

    def exist_cloud_formation(self, cf):
        exist = False
        stack_summaries = cf.describe_stacks()['Stacks']
        if len(stack_summaries) > 0:
            for StackSummary in stack_summaries:
                if StackSummary['StackName'] == self.__stackName:
                    exist = True
                    break
                else:
                    exist = False
        return exist
