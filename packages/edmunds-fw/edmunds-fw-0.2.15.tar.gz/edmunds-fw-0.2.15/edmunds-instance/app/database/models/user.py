
from edmunds.database.model import mapper, relationship, backref
from edmunds.auth.tables.usertable import UserTable
from edmunds.auth.tables.userrolestable import UserRolesTable
from edmunds.auth.models.user import User as EdmundsUser
from app.database.models.role import Role


class User(EdmundsUser):
    """
    User Model
    """
    __table__ = UserTable

    def __init__(self, id, email=None, password=None, active=None, confirmed_at=None):
        """
        Constructor
        :param id:              The id
        :param email:           The email
        :param password:        The hashed password
        :param active:          Active or inactive
        :param confirmed_at:    Confirmed account at
        """
        super(User, self).__init__(
            id,
            email=email,
            password=password,
            active=active,
            confirmed_at=confirmed_at
        )


mapper(User, UserTable, properties={
    'roles': relationship(Role, backref=backref('users', lazy='dynamic'), secondary=UserRolesTable)
})
