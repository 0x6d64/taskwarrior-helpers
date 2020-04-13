#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy

class UrgencyData(object):
    def __init__(self, allow_negative_values=False):
        """
        Container for urgency data that can be read from a dict
        :param allow_negative_values: set to True to treat negative value like 0
        """
        self._data = []
        self._urgencies = []
        self.allow_negative_values = allow_negative_values
        pass

    @property
    def average_urgency(self):
        average = None
        if self.task_count != 0:
            average = numpy.average(self.get_urgencies())
        return average

    @property
    def median_urgency(self):
        median = None
        if self.task_count != 0:
            median = numpy.median(self.get_urgencies())
        return median

    def get_urgencies(self):
        retval = self._urgencies
        if not self.allow_negative_values:
            retval = [val if val > 0 else 0 for val in self._urgencies]
        return retval

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

    def parse_data(self, json_data):
        for item in json_data:
            self._data.append(item)
        self._update_data()
