from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase
from functions.cloudformation import Cloudformation

class TestDistilDeploy(TestCase):

    def setUp(self):
        self.__account = "sgm"
        self.__resource = "cloudformation"
        self.__role = "distil-dns"

    def test_should_show_stackname_in_pre(self):
        self.__given_arguments_pre()
        self.__when_want_stackname_pre()
        self.__then_assert_stackname_pre_is_correct()

    def test_should_show_stackname_in_pro(self):
        self.__given_arguments_pro()
        self.__when_want_stackname_pro()
        self.__then_assert_stackname_pro_is_correct()

    def __given_arguments_pre(self):
        self.__environment_pre = 'pre'
        self.__number_pre = '9'
        self.__test_cloudformation_pre = Cloudformation(self.__account, self.__environment_pre, self.__number_pre, self.__resource, self.__role)

    def __given_arguments_pro(self):
        self.__environment_pro = 'pro'
        self.__number_pro = ''
        self.__test_cloudformation_pro = Cloudformation(self.__account, self.__environment_pro, self.__number_pro, self.__resource, self.__role)

    def __when_want_stackname_pre(self):
        self.__stackNamePre = self.__test_cloudformation_pre.get_stackname()

    def __when_want_stackname_pro(self):
        self.__stackNamePro = self.__test_cloudformation_pro.get_stackname()

    def __then_assert_stackname_pro_is_correct(self):
        self.assertEqual(self.__stackNamePro, self.__environment_pro + "-distil-dns")

    def __then_assert_stackname_pre_is_correct(self):
        self.assertEqual(self.__stackNamePre, self.__environment_pre + "-distil-dns-" + self.__number_pre)
