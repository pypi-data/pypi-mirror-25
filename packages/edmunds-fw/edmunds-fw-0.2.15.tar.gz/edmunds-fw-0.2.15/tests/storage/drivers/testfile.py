
from tests.testcase import TestCase
import os
import mock


class TestFile(TestCase):
    """
    Test the File
    """

    def set_up(self):
        """
        Set up the test case
        """

        super(TestFile, self).set_up()

        self.prefix = self.rand_str(20) + '.'
        self.storage_directory = os.sep + 'storage' + os.sep
        self.clear_paths = []

    def tear_down(self):
        """
        Tear down the test case
        """

        super(TestFile, self).tear_down()

        # Remove all profiler files
        for directory in self.clear_paths:
            for root, subdirs, files in os.walk(directory):
                for file in files:
                    if file.startswith(self.prefix):
                        os.remove(os.path.join(root, file))

    def test_file(self):
        """
        Test the file
        """

        string = self.rand_str(20)

        # Write config
        self.write_config([
            "from edmunds.storage.drivers.file import File \n",
            "from logging import WARNING \n",
            "APP = { \n",
            "   'storage': { \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'file',\n",
            "               'driver': File,\n",
            "               'directory': '%s',\n" % self.storage_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "               'files_path': 'files',\n",
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "   'log': { \n",
            "       'instances': [ \n",
            "       ], \n",
            "   }, \n",
            "} \n",
        ])

        # Create app
        app = self.create_application()
        directory = app.fs().path(None)
        self.clear_paths.append(directory)
        self.assert_equal(self.storage_directory, app.config('app.storage.instances')[0]['directory'])
        self.assert_equal(self.prefix, app.config('app.storage.instances')[0]['prefix'])

        # Write
        stream = app.fs().write_stream('nice.txt')
        try:
            stream.write(string)
        finally:
            stream.close()

        # Read
        stream = app.fs().read_stream('nice.txt')
        try:
            self.assert_in(string, stream.read())
        finally:
            stream.close()

        # Copy
        self.assert_true(app.fs().copy('nice.txt', 'nice2.txt'))
        stream = app.fs().read_stream('nice2.txt')
        try:
            self.assert_in(string, stream.read())
        finally:
            stream.close()

        # Exists and delete
        self.assert_true(app.fs().exists('nice2.txt'))
        self.assert_true(app.fs().delete('nice2.txt'))
        self.assert_false(app.fs().exists('nice2.txt'))

        # Read stream non existing
        self.assert_false(app.fs().read_stream('nice2.txt'))
        with self.assert_raises(IOError):
            app.fs().read_stream('nice2.txt', raise_errors=True)

        # Copy non existing
        self.assert_false(app.fs().copy('nice2.txt', 'nice.txt'))
        with self.assert_raises(IOError):
            app.fs().copy('nice2.txt', 'nice.txt', raise_errors=True)

        # Delete non existing
        self.assert_false(app.fs().delete('nice2.txt'))
        with self.assert_raises(OSError):
            app.fs().delete('nice2.txt', raise_errors=True)

    def test_copy_error(self):
        """
        Test error scenario for copy
        :return:    void
        """

        string = self.rand_str(20)

        # Write config
        self.write_config([
            "from edmunds.storage.drivers.file import File \n",
            "from logging import WARNING \n",
            "APP = { \n",
            "   'storage': { \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'file',\n",
            "               'driver': File,\n",
            "               'directory': '%s',\n" % self.storage_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "   'log': { \n",
            "       'instances': [ \n",
            "       ], \n",
            "   }, \n",
            "} \n",
            ])

        # Create app
        app = self.create_application()
        directory = app.fs().path(None)
        self.clear_paths.append(directory)

        # Write
        stream = app.fs().write_stream('nice.txt')
        try:
            stream.write(string)
        finally:
            stream.close()

        # Copy
        with mock.patch('shutil.copy2', side_effect=IOError()):
            self.assert_false(app.fs().copy('nice.txt', 'nice2.txt'))
            self.assert_false(app.fs().copy('nice.txt', 'nice2.txt', raise_errors=False))

            with self.assert_raises(IOError):
                app.fs().copy('nice.txt', 'nice2.txt', raise_errors=True)

    def test_delete_error(self):
        """
        Test delete scenario for error
        :return:    void
        """

        string = self.rand_str(20)

        # Write config
        self.write_config([
            "from edmunds.storage.drivers.file import File \n",
            "from logging import WARNING \n",
            "APP = { \n",
            "   'storage': { \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'file',\n",
            "               'driver': File,\n",
            "               'directory': '%s',\n" % self.storage_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "   'log': { \n",
            "       'instances': [ \n",
            "       ], \n",
            "   }, \n",
            "} \n",
            ])

        # Create app
        app = self.create_application()
        directory = app.fs().path(None)
        self.clear_paths.append(directory)

        # Write
        stream = app.fs().write_stream('nice.txt')
        try:
            stream.write(string)
        finally:
            stream.close()

        # Copy
        with mock.patch('os.remove', side_effect=IOError()):
            self.assert_false(app.fs().delete('nice.txt'))
            self.assert_false(app.fs().delete('nice.txt', raise_errors=False))

            with self.assert_raises(IOError):
                app.fs().delete('nice.txt', raise_errors=True)

    def test_path(self):
        """
        Test path function
        :return:    void
        """

        # Write config
        self.write_config([
            "from edmunds.storage.drivers.file import File \n",
            "from logging import WARNING \n",
            "APP = { \n",
            "   'storage': { \n",
            "       'instances': [ \n",
            "           { \n",
            "               'name': 'file',\n",
            "               'driver': File,\n",
            "               'directory': '%s',\n" % self.storage_directory,
            "               'prefix': '%s',\n" % self.prefix,
            "           }, \n",
            "       ], \n",
            "   }, \n",
            "   'log': { \n",
            "       'instances': [ \n",
            "       ], \n",
            "   }, \n",
            "} \n",
            ])

        # Create app
        app = self.create_application()
        directory = os.path.join(app.root_path, self.storage_directory[1:-1])

        data = [
            ('%s/files/' % directory, '%s/files/' % directory, None),
            ('%s/' % directory, '%s/' % directory, '/'),

            ('%s/files/%snice' % (directory, self.prefix), '%s/files/nice' % directory, 'nice'),
            ('%s/files/%snice.txt' % (directory, self.prefix), '%s/files/nice.txt' % directory, 'nice.txt'),
            ('%s/files/sub/directory/%snice.txt' % (directory, self.prefix), '%s/files/sub/directory/nice.txt' % directory, 'sub/directory/nice.txt'),

            ('%s/%snice' % (directory, self.prefix), '%s/nice' % directory, '/nice'),
            ('%s/%snice.txt' % (directory, self.prefix), '%s/nice.txt' % directory, '/nice.txt'),
            ('%s/sub/directory/%snice.txt' % (directory, self.prefix), '%s/sub/directory/nice.txt' % directory, '/sub/directory/nice.txt'),

            ('%s/files/nice/' % directory, '%s/files/nice/' % directory, 'nice/'),
            ('%s/files/nice.txt/' % directory, '%s/files/nice.txt/' % directory, 'nice.txt/'),
            ('%s/files/sub/directory/nice.txt/' % directory, '%s/files/sub/directory/nice.txt/' % directory, 'sub/directory/nice.txt/'),

            ('%s/nice/' % directory, '%s/nice/' % directory, '/nice/'),
            ('%s/nice.txt/' % directory, '%s/nice.txt/' % directory, '/nice.txt/'),
            ('%s/sub/directory/nice.txt/' % directory, '%s/sub/directory/nice.txt/' % directory, '/sub/directory/nice.txt/'),
        ]

        for expected, expected_no_prefix, given in data:
            self.assert_equal(expected, app.fs().path(given))
            self.assert_equal(expected, app.fs('file').path(given))
            self.assert_equal(expected_no_prefix, app.fs().path(given, prefix=''))
            self.assert_equal(expected_no_prefix, app.fs('file').path(given, prefix=''))
