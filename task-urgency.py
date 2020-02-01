#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
calculate urgency values for taskwarrior tasks
"""
import argparse
import subprocess
import json


class UrgencyData(object):
    def __init__(self):
        self._data = []
        pass

    @property
    def average_urgency(self):
        average = None
        if self.task_count != 0:
            average = self.sum_urgency / self.task_count
        return average

    def _get_urgency_list(self):
        return [item.get('urgency') for item in self._data]

    @property
    def max_urgency(self):
        return max(self._get_urgency_list())

    @property
    def task_count(self):
        return len(self._get_urgency_list())

    @property
    def sum_urgency(self):
        return sum(self._get_urgency_list())

    def parse_json(self, json_data):
        for item in json_data:
            self._data.append(item)


def get_json(filter):
    command = ['task', filter, 'export']
    sp = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = sp.communicate()
    json_data = json.loads(out)
    return json_data

def print_condensed(data):
    print('avg/max/count: {:.1f}/{:.1f}/{}'.format(
        data.average_urgency, data.max_urgency, data.task_count))


def run_main(args, filterstring='+PENDING'):
    json_raw = get_json(filterstring)
    data = UrgencyData()
    data.parse_json(json_raw)

    print_condensed(data)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    exit_code = run_main(args)

    exit(exit_code)
