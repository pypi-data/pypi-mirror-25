
from tests.testcase import TestCase
import os


class TestTimedFile(TestCase):
    """
    Test the TimedFile
    """

    def set_up(self):
        """
        Set up the test case
        """

        super(TestTimedFile, self).set_up()

        self.prefix = self.rand_str(20) + '.'
        self.prefix2 = self.rand_str(20) + '.'
        self.storage_directory = os.sep + 'storage' + os.sep
        self.logs_directory = os.sep + 'logs' + os.sep
        self.clear_paths = []

    def tear_down(self):
        """
        Tear down the test case
        """

        super(TestTimedFile, self).tear_down()

        # Remove all profiler files
        for directory in self.clear_paths:
            for root, subdirs, files in os.walk(directory):
                for file in files:
                    if file.startswith(self.prefix):
                        os.remove(os.path.join(root, file))

    def test_timed_file(self):
        """
        Test the timed file
        """

        info_string = 'info_%s' % self.rand_str(20)
        warning_string = 'warning_%s' % self.rand_str(20)
        error_string = 'error_%s' % self.rand_str(20)

        # Write config
        self.write_config([
            "from edmunds.storage.drivers.file import File as StorageFile \n",
            "from edmunds.log.drivers.timedfile import TimedFile \n",
            "from logging import WARNING \n",
            "APP = { \n",
            "   'debug': False, \n",
            "   'storage': { \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'file',\n",
            "               'driver': StorageFile,\n",
            "               'directory': '%s',\n" % self.storage_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "   'log': { \n",
            "       'enabled': True, \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'timedfile',\n",
            "               'driver': TimedFile,\n",
            "               'directory': '%s',\n" % self.logs_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "               'level': WARNING,\n"
            "               'when': 'h',\n"
            "               'interval': 1,\n"
            "               'backup_count': 0,\n"
            "               'format': '%(message)s',\n"
            "           }, \n",
            "           { \n",
            "               'name': 'timedfile2',\n",
            "               'driver': TimedFile,\n",
            "               'directory': '%s',\n" % self.logs_directory,
            "               'prefix': '%s',\n" % self.prefix2,
            "               'level': WARNING,\n"
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "} \n",
        ])

        # Create app and fetch stream
        app = self.create_application()
        directory = app.fs().path(self.logs_directory)
        self.clear_paths.append(directory)
        self.assert_equal(self.logs_directory, app.config('app.log.instances')[0]['directory'])
        self.assert_equal(self.prefix, app.config('app.log.instances')[0]['prefix'])

        # Add route
        info_rule = '/' + self.rand_str(20)
        @app.route(info_rule)
        def handle_info_route():
            app.logger.info(info_string)
            return ''
        warning_rule = '/' + self.rand_str(20)
        @app.route(warning_rule)
        def handle_warning_route():
            app.logger.warning(warning_string)
            return ''
        error_rule = '/' + self.rand_str(20)
        @app.route(error_rule)
        def handle_error_route():
            app.logger.error(error_string)
            return ''

        with app.test_client() as c:

            # Check file
            self.assert_false(self._is_in_log_files(app, directory, info_string))
            self.assert_false(self._is_in_log_files(app, directory, warning_string))
            self.assert_false(self._is_in_log_files(app, directory, error_string))

            # Call route
            c.get(info_rule)
            c.get(warning_rule)
            c.get(error_rule)

            # Check file
            self.assert_false(self._is_in_log_files(app, directory, info_string))
            self.assert_true(self._is_in_log_files(app, directory, warning_string))
            self.assert_true(self._is_in_log_files(app, directory, error_string))

    def _is_in_log_files(self, app, directory, string, starts_with = None):
        """
        Check if string is in log files
        :param app:             The app to work with
        :type  app:             Application
        :param directory:       The directory to check
        :type  directory:       str
        :param string:          The string to check
        :type  string:          str
        :param starts_with:     The filename starts with
        :type  starts_with:     str
        :return:                Is in file
        :rtype:                 boolean
        """

        if starts_with is None:
            starts_with = self.prefix

        # Fetch files
        log_files = []
        for root, subdirs, files in os.walk(directory):
            for file in files:
                if file.startswith(starts_with):
                    log_files.append(os.path.join(self.logs_directory, file))

        # Check files
        occurs = False
        for file in log_files:
            f = app.fs().read_stream(file)

            try:
                if string in f.read():
                    occurs = True
                    break
            finally:
                f.close()

        return occurs
