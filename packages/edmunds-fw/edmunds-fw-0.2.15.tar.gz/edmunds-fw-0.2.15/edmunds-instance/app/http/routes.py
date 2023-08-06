
from app.http.controllers.homecontroller import HomeController
from app.http.middleware.myrequestmiddleware import MyRequestMiddleware


def route(app):
    """
    Define the routes in the application
    :rtype: None
    """

    app.route('/', middleware=[MyRequestMiddleware], uses=(HomeController, 'get_index'))
