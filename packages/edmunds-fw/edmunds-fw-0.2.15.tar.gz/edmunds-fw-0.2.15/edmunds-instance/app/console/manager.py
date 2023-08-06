
from edmunds.console.manager import Manager as EdmundsManager
from edmunds.foundation.testing.testcommand import TestCommand
from edmunds.foundation.database.migratecommand import MigrateCommand
from app.console.commands.helloworldcommand import HelloWorldCommand


class Manager(EdmundsManager):
    """
    The manager to control the command-line usage of the application
    """

    def add_default_commands(self):
        """
        Adds the shell and runserver default commands. To override these,
        simply add your own equivalents using add_command or decorators.
        """

        super(Manager, self).add_default_commands()

        self.add_command('test', TestCommand())
        self.add_command('db', MigrateCommand(self.app))

        self.add_command('helloworld', HelloWorldCommand())
