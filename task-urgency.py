#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
calculate urgency values for taskwarrior tasks
"""
import argparse

from twhelpers.urgency import UrgencyData


def print_condensed(data):
    print('median/avg/sum/count: {:.1f}/{:.1f}/{:.1f}/{}'.format(
        data.median_urgency, data.average_urgency, data.sum_urgency, data.task_count))


def run_main(args, filterstring='+PENDING'):
    data = UrgencyData(allow_negative_values=True)
    data.get_data(filterstring)

    print_condensed(data)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    exit_code = run_main(args)

    exit(exit_code)
