
from edmunds.gae.gaetestcase import GaeTestCase as EdmundsGaeTestCase
from bootstrap.myapp import bootstrap
import os


class GaeTestCase(EdmundsGaeTestCase):
    """
    A UnitTest Gae Test Case
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
