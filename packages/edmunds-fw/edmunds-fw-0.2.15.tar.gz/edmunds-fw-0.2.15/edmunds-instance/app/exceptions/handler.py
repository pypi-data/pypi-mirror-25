
from edmunds.exceptions.handler import Handler as EdmundsHandler


class Handler(EdmundsHandler):
    """
    Exception handler
    """

    def report(self, exception):
        """
        Report the exception
        :param exception:   The exception
        :type  exception:   Exception
        """

        super(Handler, self).report(exception)

    def render(self, exception):
        """
        Render the exception
        :param exception:   The exception
        :type  exception:   Exception
        :return:            The response
        """

        return super(Handler, self).render(exception)
