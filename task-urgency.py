#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
calculate urgency values for taskwarrior tasks
"""
import argparse
import subprocess
import json
from twhelpers.urgency import UrgencyData



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
    data = UrgencyData(allow_negative_values=True)
    data.parse_data(get_json(filterstring))

    print_condensed(data)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    exit_code = run_main(args)

    exit(exit_code)
