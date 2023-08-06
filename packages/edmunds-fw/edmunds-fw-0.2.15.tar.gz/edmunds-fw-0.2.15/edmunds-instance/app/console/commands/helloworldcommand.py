
from edmunds.console.command import Command


class HelloWorldCommand(Command):
    """
    Prints Hello World!
    """

    def run(self):
        """
        Run the command
        :return:    void
        """

        print('Hello World!')
