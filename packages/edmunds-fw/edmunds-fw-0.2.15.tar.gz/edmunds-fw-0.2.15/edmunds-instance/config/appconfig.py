
from app.exceptions.handler import Handler as ExceptionHandler
from app.database.models.user import User
from app.database.models.role import Role


APP = {

    # ------------------------------------------------------------
    # General
    # ------------------------------------------------------------
    #
    # General application configuration is defined here.
    #

    'name': 'My App',



    # ------------------------------------------------------------
    # Exceptions
    # ------------------------------------------------------------
    #
    # Exception-handling is configured here. They can be handled
    # with custom handlers when provided.
    #

    'exceptions':
    {
        'handler': ExceptionHandler,
    },



    # ------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------
    #
    # Authentication is configured here.
    #

    'auth':
    {
        'enabled': False,
        'models': {
            'user': User,
            'role': Role,
        },
    },

}
