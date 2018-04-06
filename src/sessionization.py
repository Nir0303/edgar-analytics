# /usr/bin/env python
"""
Main module for edgar analytics application
"""

import csv
import datetime
import argparse
from collections import OrderedDict


mapping = {'ip': 0, 'date': 1, 'time': 2, 'zone': 3, 'cik': 4,
           'accession': 5, 'extention': 6, 'code': 7, 'size': 8,
           'idx': 9, 'norefer': 10, 'noagent': 11, 'find': 12,
           'crawler': 13, 'browser': 14}


def parse_args():
    """
        function for argument parsing
        :return: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="input files to process", type=str)
    parser.add_argument("--inactivity_file", "-a", help="inactivity file", type=str)
    parser.add_argument("--output", "-o", help="output file to write process data", type=str)
    parser.add_argument("--log_level", "-l", help="Set loglevel for debugging and analysis",
                         default="INFO")
    args = parser.parse_args()
    return args


def time_difference_in_seconds(start_time, end_time):
    """
    Calculate time difference between start_time and end_time in seconds
    :param start_time: Start time of job or process
    :param end_time: End Time of job or process
    :return: time difference in seconds
    """
    timediff = start_time - end_time
    return int(timediff.total_seconds())


class Record(object):
    """
    User Defined type for each edgar record
    """
    def __init__(self, ip, start_time, document):
        """
        :param ip: ip address, unique identifier for records
        :param start_time: Start timestamp of session
        :param document: document been requested by session
        """
        self.ip = ip
        self.start_time = start_time
        self.document = [document]
        self.end_time = self.start_time

    def insert(self, document,  end_time):
        """
        Update record details if record already been tracked
        :param document: new document been requested by session
        :param end_time: new session timestamp
        :return:
        """
        self.end_time = max(self.end_time, end_time)
        self.document.append(document)

    @property
    def time_diff(self):
        """
        Calculate activity time,
        difference between start time and end time
        :return: user session time in seconds
        """
        _time_diff = time_difference_in_seconds(self.end_time, self.start_time) + 1
        return str(_time_diff)

    def __repr__(self):
        """
        Override repr special method for printing or writing data
        :return: str representation of Record object
        """
        return self.ip + ',' + str(self.start_time) + ','  \
                 + str(self.end_time)+ ',' + \
               self.time_diff + ',' + str(len(self.document))

    def __eq__(self, other):
        """
        override equal operator during comparsion
        :param other: other object for comparison
        :return:
        """
        return self.ip == other


class App(object):
    """
    main application for streaming data and processing data
    """
    def __init__(self, input_file=None, output_file=None, inactivity_file=None):
        """
        :param input_file: log file to read session details
        :param output_file: output file to save processed information
        :param inactivity_file: inactivity session details file
        """
        self.logs = OrderedDict()
        self.input_file = 'input/log.csv' if not input_file else input_file
        self.output_file = 'output/sessionization.txt' if not output_file else output_file
        self.inactivity_file = 'input/inactivity_period.txt' if not inactivity_file else inactivity_file
        self.current_record_time = None
        self.current_ip = None

    @property
    def inactivity_period(self):
        """
        inactivity_period property
        :return: inactivity period in seconds
        """
        with open('input/inactivity_period.txt') as f:
            _inactivity_period = int(f.read().replace(',', ''))
        return _inactivity_period

    def read_files(self):
        """
        Generator to read log file
        :return: each line of log file
        """
        with open(self.input_file) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=",")
            for index, row in enumerate(csvreader):
                if index == 0:
                    continue
                if len(row) != 15:
                    print("Ignore invalid record as it is having insufficient information")
                    print(row)
                    continue

                yield row

    def write_output(self):
        """
        static coroutine write session output
        :return: None
        """
        with open(self.output_file, 'w') as f:
            while True:
                line = yield
                f.write(line)
                f.write('\n')

    def insert_log(self, ip, row):
        """
        insert log for tracking
        :param ip: ip address of session
        :param row: current processing record
        :return: None
        """
        self.logs[ip] = Record(ip=row[mapping['ip']],
                                start_time=self.current_record_time,
                                document=row[mapping['cik']] + '-' +
                                         row[mapping['accession']] + '-' + row[mapping['extention']])

    def update_log(self, ip, row):
        """
        Update log which already been tracked
        :param ip: ip address of session
        :param row: current processing record
        :return: None
        """
        self.logs[ip].insert(end_time=self.current_record_time,
                             document=row[mapping['cik']] + '-' +
                                      row[mapping['accession']] + '-' + row[mapping['extention']])

    def write_log(self, check_time=None):
        """
        Write log to output file and remove it from tracking
        :param check_time: current session timestamp to check for possible session expirations
        :return:
        """
        keys = list(self.logs.keys())
        for key in keys:
            if check_time:
                time_diff = time_difference_in_seconds(check_time, self.logs[key].end_time)
                # check if the user session has been ended
                if time_diff > self.inactivity_period:
                    self.output.send(str(self.logs[key]))
                    del self.logs[key]
            else:
                self.output.send(str(self.logs[key]))
                del self.logs[key]

    def run(self):
        """
        Driver method  for the application
        :return:
        """
        self.output = self.write_output()
        next(self.output)
        for index, row in enumerate(self.read_files()):
            # current record timestamp and ip address
            self.current_record_time = datetime.datetime.strptime(row[mapping['date']] + ' '
                                                                  + row[mapping['time']],
                                                                  '%Y-%m-%d %H:%M:%S')
            self.current_ip = row[mapping['ip']]
            if not index:
                # first record insert
                self.insert_log(self.current_ip, row)
                check_time = self.current_record_time
            elif self.current_record_time != check_time:
                # timestamp of current record has changed, check for possible session expirations
                check_time = self.current_record_time
                self.write_log(check_time)
                if self.logs.get(self.current_ip, None):
                    self.update_log(self.current_ip, row)
                else:
                    self.insert_log(self.current_ip, row)
            else:
                if self.logs.get(self.current_ip, None):
                    self.update_log(self.current_ip, row)
                else:
                    self.insert_log(self.current_ip, row)
        else:
            # file has been iterated, write remaining records to file.
            self.write_log()


if __name__ == '__main__':
    try:
        app_start_time = datetime.datetime.now()
        args = parse_args()
        print("Starting Edgar streaming application at {}".format(app_start_time))
        app = App(input_file=args.input, output_file=args.output, inactivity_file=args.inactivity_file)
        print("Processing Edgar data with {} file".format(app.input_file))
        app.run()
        print("Processed Edgar data , Output is stored in {}".format(app.output_file))
        app_end_time = datetime.datetime.now()
        print("Edgar streaming application ended at {}".format(app_end_time))
        print("Total time taken in seconds {}".format(time_difference_in_seconds(app_start_time, app_end_time)+1))
    except FileNotFoundError as e:
        print("Application failed to process data")
        print("Input file {} is not found, please check input files before processing".format(app.input_file))
        exit(1)
    except KeyError as e:
        print("Unable to find key {} in logs".format(app.current_ip))
        exit(1)
    except Exception as e:
        print("Application failed with unknown error {}" .format(e))
