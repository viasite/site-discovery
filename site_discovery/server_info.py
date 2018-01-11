import argparse
import json
import signal
import subprocess
import os
import time
import sys
import yaml
from influxdb import line_protocol


def signal_handler(signal, frame):
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='server-info')
    parser.add_argument('--format',
                        action='store', dest='output_format', default='console',
                        help='Output format (console, json, line')
    parser.add_argument('--group',
                        action='append', dest='groups', default=['main'],
                        help='Groups of server-info tests')

    args = parser.parse_args()

    server_info = ServerInfo(args)
    server_info.prepare()
    server_info.run()
    server_info.output()


class ServerInfo():
    def __init__(self, args):
        self.groups = args.groups
        self.output_format = args.output_format
        self.tests = []
        self.info = {}
        self.reset()

    def prepare(self):
        self.tests = self.get_tests()

    def get_all_tests(self):
        tests_config = {}
        paths = [
            '/etc/server-info.yml',
            os.path.expanduser('~') + '/server-info.yml'
        ]

        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    tests_config = yaml.load(f)

        if not tests_config:
            print("No server-info.yml found, or empty, aborting.")
            sys.exit(1)

        for t in tests_config['tests']:
            # normalize config
            if 'groups' in t:
                if not isinstance(t['groups'], (list)):
                    t['groups'] = [t['groups']]
            else:
                t['groups'] = []

        return tests_config['tests']

    def get_tests(self):
        tests_config = self.get_all_tests()
        groups = self.groups
        filtered = []

        if 'all' in groups:
            return tests_config

        for t in tests_config:
            # filter by groups intersection
            intersect = list(set(groups) & set(t['groups']))
            if intersect:
                filtered.append(t)
        return filtered

    def reset(self):
        for test in self.tests:
            test.result = None
            test.time = 0
        self._results = []

    def get_info(self):
        info = {}

        tests = self.get_tests()
        results = []
        for test in tests:
            (out, err, time) = self.run_command(test['command'])
            result = test
            result['result'] = int(out) if test['type'] == 'integer' else out
            result['time'] = time

            results.append(result)

            if self.output_format == 'console':
                print '%s: %s (%s)' % (result['name'], result['result'], result['time'])

        info['results'] = results
        return info

    def run_command(self, command):
        if command is not None:
            started = time.time()
            proc = subprocess.Popen(
                command, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            command_time = round(time.time() - started, 1)
            return (out.strip() if out else None, err.strip() if err else None, command_time)

    def run(self):
        self.info = self.get_info()

    def output(self):
        if self.output_format == 'console':
            return

        elif self.output_format == 'json':
            json_raw = json.dumps(self.info)
            print(json_raw)

        if self.output_format == 'line':
            measurement = 'server_info'
            fields = {}
            tags = {}
            # for t in self.info['results']:
            #     tags[t['name']] = t['result']

            for t in self.info['results']:
                if t['type'] == 'integer':
                    fields[t['name']] = t['result']

            #tags_raw = ['%s=%s' % (k,v) for k,v in tags.iteritems()]
            #fields = {'zxc': 3, 'qwe': 4}
            #line = '%s,%s %s %s' % (measurement, tags_raw.join(','), fields_raw, timestamp)
            # print line

            data = {'points': [{
                'measurement': measurement,
                'tags': tags,
                'fields': fields
            }]}

            print line_protocol.make_lines(data)


if __name__ == '__main__':
    main()
