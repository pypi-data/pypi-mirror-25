
from edmunds.foundation.applicationmiddleware import ApplicationMiddleware


class MyApplicationMiddleware(ApplicationMiddleware):
    """
    My Application Middleware
    """

    def handle(self, environment, startResponse):
        """
        Handle the middleware
        :param environment:     The environment
        :type  environment:     Environment
        :param startResponse:   The application
        :type  startResponse:   flask.Response
        """

        return super(MyApplicationMiddleware, self).handle(environment, startResponse)
