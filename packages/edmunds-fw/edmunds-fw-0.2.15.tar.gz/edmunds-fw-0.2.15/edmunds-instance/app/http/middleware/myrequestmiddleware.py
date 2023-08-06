
from edmunds.http.requestmiddleware import RequestMiddleware


class MyRequestMiddleware(RequestMiddleware):
    """
    My Request Middleware
    """

    def before(self):
        """
        Handle before the request
        """

        return super(MyRequestMiddleware, self).before()

    def after(self, response):
        """
        Handle after the request
        :param response:    The request response
        :type  response:    flask.Response
        :return:            The request response
        :rtype:             flask.Response
        """

        return super(MyRequestMiddleware, self).after(response)
