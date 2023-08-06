
from edmunds.http.controller import Controller


class HomeController(Controller):
    """
    My Home Controller
    """

    def get_index(self):
        """
        Index page
        """

        return 'Hello World!'
