
from edmunds.database.model import mapper
from edmunds.auth.tables.roletable import RoleTable
from edmunds.auth.models.role import Role as EdmundsRole


class Role(EdmundsRole):
    """
    Role Model
    """
    __table__ = RoleTable

    def __init__(self, id, name=None, description=None):
        """
        Constructor
        :param id:          The id
        :param name:        The name
        :param description: The description
        """
        super(Role, self).__init__(
            id,
            name=name,
            description=description
        )


mapper(Role, RoleTable)
