import os
import csv
import heapq
import datetime
from collections import OrderedDict

DEFAULT_OFFLINE_TIME = 1

mapping = {'ip': 0, 'date': 1, 'time': 2, 'zone': 3, 'cik': 4, 'accession': 5, 'extention': 6, 'code': 7, 'size': 8,
           'idx': 9, 'norefer': 10, 'noagent': 11, 'find': 12, 'crawler': 13, 'browser': 14}

class Record(object):
    def __init__(self, ip, start_date, start_time, document):
        self.ip = ip
        self.start_time = datetime.datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M:%S')
        self.document = [document]
        self.end_time = self.start_time + datetime.timedelta(seconds=1)

    def insert(self, document, end_date, end_time):
        self.end_time = max(self.end_time, datetime.datetime.strptime(end_date + ' ' + end_time, '%Y-%m-%d %H:%M:%S'))
        self.document.append(document)

    @property
    def time_diff(self):
        _time_diff = self.end_time - self.start_time
        return str(_time_diff.seconds)

    def __repr__(self):
        return self.ip + ',' + str(self.start_time.date()) + ',' + str(self.start_time.time()) + ' ' \
                 + str(self.end_time.date()) + ',' + str(self.end_time.time()) + ',' + str(len(self.document)) + ',' + self.time_diff

    def __eq__(self, other):
        return self.ip == other


class App(object):
    def __init__(self):
        self.logs = OrderedDict()
        self.current_time = None
        self.output = self.write_output()
        next(self.output)

    def read_files(self):
        for dir_path, sub_dirs, file_names in os.walk('input/'):
            for file_name in sorted (file_names):
                if file_name != 'log_small.csv':
                    continue
                with open ('input/log_small.csv') as csvfile:
                    csvreader = csv.reader (csvfile, delimiter=",")
                    for index, row in enumerate (csvreader):
                        if index == 0:
                            continue
                        yield row

    def write_output(self):
        with open('output/output.txt', 'w') as f:
            while True:
                line = yield
                f.write (line)
                f.write ('\n')

    def insert_log(self, ip, row):
        self.logs[ip] = [self.current_record_time,
                                Record(ip=row[mapping['ip']], start_date=row[mapping['date']],
                                    start_time=row[mapping['time']],
                                    document=row[mapping['extention']])]

    def update_log(self, ip, row):

        self.logs[ip][0] = self.current_record_time
        self.logs[ip][1].insert(end_date=row[mapping['date']],
                                end_time=row[mapping['time']],
                                document=row[mapping['extention']])

    def update_output_file(self,check_time=None):
        keys = list(self.logs.keys())
        for key in keys:
            if check_time:
                time_diff = check_time - self.logs[key][0]
                if time_diff.seconds > DEFAULT_OFFLINE_TIME:
                    self.output.send(str(self.logs[key][1]))
                    del self.logs[key]
            else:
                self.output.send(str(self.logs[key][1]))
                del self.logs[key]

    def run(self):

        for index, row in enumerate(self.read_files()):
            self.current_record_time = datetime.datetime.strptime (row[mapping['date']] + ' ' + row[mapping['time']], '%Y-%m-%d %H:%M:%S')
            if not index:
                self.insert_log(row[mapping['ip']],row)
                check_time = self.current_record_time
            elif self.current_record_time != check_time:
                check_time = self.current_record_time
                self.update_output_file()
                if self.logs.get(row[mapping['ip']], None):
                    self.update_log(row[mapping['ip']], row)
                else:
                    self.insert_log(row[mapping['ip']], row)

            else:
                if self.logs.get(row[mapping['ip']], None):
                    self.update_log(row[mapping['ip']], row)
                else:
                    self.insert_log(row[mapping['ip']], row)

        else:
            self.update_output_file()


if __name__ == '__main__':
    app = App()
    app.run()