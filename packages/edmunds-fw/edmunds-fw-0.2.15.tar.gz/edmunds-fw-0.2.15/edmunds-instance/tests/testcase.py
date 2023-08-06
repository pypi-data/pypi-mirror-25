
from edmunds.foundation.testing.testcase import TestCase as EdmundsTestCase
from bootstrap.myapp import bootstrap
import os


class TestCase(EdmundsTestCase):
    """
    A UnitTest Test Case
    """

    def create_application(self, environment='testing'):
        """
        Create the application for testing
        :param environment: Environment
        :type environment:  str
        :return:            edmunds.application.Application
        """

        os.environ['APP_ENV'] = environment

        return bootstrap()
