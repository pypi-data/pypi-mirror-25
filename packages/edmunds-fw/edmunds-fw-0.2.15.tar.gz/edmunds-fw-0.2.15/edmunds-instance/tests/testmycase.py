
from tests.testcase import TestCase


class TestMyCase(TestCase):
    """
    Test my case
    """

    def test_nothing(self):
        """
        Test nothing
        :return:    void
        """

        self.assert_equal(1, 1)
