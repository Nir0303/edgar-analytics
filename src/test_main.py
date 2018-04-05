# /usr/bin/env python
"""
Module to test main module
"""
import unittest
from mock import patch, PropertyMock
from main import App, Record


# pylint: disable=R0201
class TestMain(unittest.TestCase):
    """
    Class to test main module
    """

    def test_app_attributes(self):
        """
        test case to validate App attributes
        :return:
        """
        print("------------validating app attributes------------------")
        assert hasattr(App, 'read_files')
        assert hasattr(App, 'write_output')
        assert hasattr(App, 'insert_log')
        assert hasattr(App, 'update_log')
        assert hasattr(App, 'write_log')
        assert hasattr(App, 'run')
        assert isinstance(App.inactivity_period, property)

    def test_record_attributes(self):
        """
        test case to validate Record attributes
        :return:
        """
        print("------------validating record attributes------------------")
        assert hasattr(Record, 'insert')
        assert hasattr(Record, 'time_diff')
        assert isinstance(Record.time_diff, property)

    @patch('main.App.run')
    def test_run(self, run=None):
        """
        test case to validate run function
        :param run:
        :return:
        """
        print("------------validating run function------------------")
        run.return_value = 'test run'
        t = App()
        assert t.run() == 'test run'
    
    def test_record_success(self):
        """
        test case to validate record data
        :return: 
        """
        record = Record(ip='123',start_date='2017-06-30',
                        start_time='00:00:00',
                        document='test')
        record.insert(document='test', end_date='2017-06-30', end_time='00:00:00')
        assert record.start_time == record.end_time
        assert len(record.document) == 2
        assert record.time_diff == '1'
        record.insert(document='test2', end_date='2017-06-30', end_time='00:10:00')
        assert record.start_time != record.end_time
        assert len(record.document) == 3
        assert record.time_diff == '601'
        assert str(record) == '123,2017-06-30,00:00:00,2017-06-30,00:10:00,601,3'

    def test_record_failure(self):
        """
        test case to validate record data
        :return:
        """
        record = Record(ip='121', start_date='2017-06-30',
                        start_time='00:00:00',
                        document='test')
        record.insert(document='test', end_date='2017-06-30', end_time='00:00:00')
        assert len(record.document) != 1
        record.insert(document='test2', end_date='2017-07-30', end_time='00:00:00')
        assert record.start_time != record.end_time
        assert len(record.document) != 2
        assert record.time_diff != '1'

    def test_app(self):
        pass

        

if __name__ == '__main__':
    test = TestMain()
    test.test_app_attributes()
    test.test_record_attributes()
    test.test_record_success()
    test.test_record_failure()