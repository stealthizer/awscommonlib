#!/usr/bin/env python
from functions.boto_connections import AWSBotoAdapter


class Cloudformation(object):

    def __init__(self, account_name, environment, number, resource, role):
        self.__environment = environment
        self.__account_name = account_name
        self.__profile = self.__account_name + "-" + self.__environment
        self.__connection = AWSBotoAdapter()
        self.__resource = resource
        self.__number = number
        self.__role = role

    def get_stackname(self):
        self.__stackName = self.__environment + "-" + self.__role
        if self.__environment == 'pre':
            self.__stackName = "{}-{}".format(self.__stackName, self.__number)
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
