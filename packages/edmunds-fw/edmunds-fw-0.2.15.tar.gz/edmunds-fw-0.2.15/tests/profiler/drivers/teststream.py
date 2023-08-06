
from tests.testcase import TestCase


class TestStream(TestCase):
    """
    Test the Stream
    """

    def test_stream(self):
        """
        Test the stream
        """

        # Write config
        self.write_config([
            "from edmunds.profiler.drivers.stream import Stream \n",
            "try: \n",
            "   from cStringIO import StringIO \n",
            "except ImportError: \n",
            "   from io import StringIO \n",
            "APP = { \n",
            "   'debug': True, \n",
            "   'profiler': { \n",
            "       'enabled': True, \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'stream',\n",
            "               'driver': Stream,\n",
            "               'stream': StringIO(),\n",
            "               'sort_by': ('time', 'calls'),\n",
            "               'restrictions': (),\n",
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "} \n",
        ])

        # Create app and fetch stream
        app = self.create_application()
        stream = app.config('app.profiler.instances')[0]['stream']

        # Add route
        rule = '/' + self.rand_str(20)
        @app.route(rule)
        def handle_route():
            return ''

        with app.test_client() as c:

            # Check stream
            self.assert_equal('', stream.getvalue())

            # Call route
            c.get(rule)

            # Check stream
            self.assert_not_equal('', stream.getvalue())
