
from tests.testcase import TestCase
from sqlalchemy.engine.base import Engine


class TestPostgreSql(TestCase):
    """
    Test PostgreSql
    """

    def test_missing_params(self):
        """
        Test missing params
        :return:    void
        """

        config = [
            "from edmunds.database.drivers.postgresql import PostgreSql \n",
            "APP = { \n",
            "   'database': { \n",
            "       'enabled': True, \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'postgresql',\n",
            "               'driver': PostgreSql,\n",
            "               'user': 'root',\n",
            "               'pass': 'root',\n",
            "               'host': 'localhost',\n",
            "               'database': 'edmunds',\n",
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "} \n",
        ]
        remove_lines = [8, 9, 10, 11]

        # Loop lines that should be individually removed
        for remove_line in remove_lines:
            new_config = config[:]
            del new_config[remove_line]

            self.write_config(new_config)

            # Create app
            app = self.create_application()

            # Error on loading of config
            with self.assert_raises_regexp(RuntimeError, 'missing some configuration'):
                app.database()

    def test_postgre_sql(self):
        """
        Test PostgreSql
        :return:    void
        """

        # Write config
        self.write_config([
            "from edmunds.database.drivers.postgresql import PostgreSql \n",
            "APP = { \n",
            "   'database': { \n",
            "       'enabled': True, \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'postgresql',\n",
            "               'driver': PostgreSql,\n",
            "               'user': 'root',\n",
            "               'pass': 'root',\n",
            "               'host': 'localhost',\n",
            "               'database': 'edmunds',\n",
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "} \n",
        ])

        # Create app
        app = self.create_application()

        # Test database
        engine = app.database()
        self.assert_is_not_none(engine)
        self.assert_is_instance(engine, Engine)

        # Test SQLAlchemy config
        self.assert_equal('postgresql://root:root@localhost:5432/edmunds', app.config('SQLALCHEMY_DATABASE_URI'))
