#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
calculate urgency values for taskwarrior tasks
"""
import argparse
import subprocess
import json
from math import floor


class UrgencyData(object):
    def __init__(self):
        self._data = []
        self._urgencies = []
        pass

    @property
    def average_urgency(self):
        average = None
        if self.task_count != 0:
            average = self.sum_urgency / self.task_count
        return average

    @property
    def median_urgency(self):
        urgencies = self.get_urgencies()
        idx = int(floor(self.task_count / 2))
        even_number_of_elements = self.task_count % 2 == 0
        if even_number_of_elements:
            median = (urgencies[idx] + urgencies[idx + 1]) / 2
        else:
            median = urgencies[idx]
        return median

    def get_urgencies(self):
        return self._urgencies

    @property
    def max_urgency(self):
        return max(self.get_urgencies())

    @property
    def task_count(self):
        return len(self.get_urgencies())

    @property
    def sum_urgency(self):
        return sum(self.get_urgencies())

    def _update_data(self):
        self._data = sorted(self._data, key=lambda k: k['urgency'])
        self._urgencies = [item.get('urgency') for item in self._data]

    def parse_json(self, json_data):
        for item in json_data:
            self._data.append(item)
        self._update_data()


def get_json(filter):
    command = ['task', filter, 'export']
    sp = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = sp.communicate()
    json_data = json.loads(out)
    return json_data


def print_condensed(data):
    print('median/avg/sum/count: {:.1f}/{:.1f}/{:.1f}/{}'.format(
        data.median_urgency, data.average_urgency, data.sum_urgency, data.task_count))


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
