# coding: utf-8

import sys
import re
import json
import traceback
from collections import OrderedDict

import numpy as np
import pandas as pd
from PySide.QtCore import QThread, Signal

from data.indicators import INDICATORS_REGISTRY, ArvStartedPatients,\
    PatientIndicator
import utils


class BaseTemplateProcessor(QThread):
    """
    Abstract base class for report template processing.
    """

    update_progress = Signal(int)
    error = Signal(str)

    def __init__(self, fuchia_database):
        super(BaseTemplateProcessor, self).__init__()
        self._fuchia_database = fuchia_database
        self._arv_started = ArvStartedPatients(self._fuchia_database)
        self._report_widget = None
        self._start_date = None
        self._end_date = None
        self.last_values = OrderedDict()
        self.last_template_values = {}

    @property
    def fuchia_database(self):
        return self._fuchia_database

    @fuchia_database.setter
    def fuchia_database(self, value):
        self._fuchia_database = value
        self._arv_started = ArvStartedPatients(self._fuchia_database)

    def get_cell_content(self, i, j):
        raise NotImplementedError()

    def get_cell_members(self, i, j):
        regex = "^\{(.+?)\}$"
        content = self.get_cell_content(i, j)
        if pd.isnull(content):
            return None
        res = re.match(regex, content)
        if not res:
            return None
        content = re.sub(r"{\s*'?(\w)", r'{"\1', content)
        content = re.sub(r",\s*'?(\w)", r',"\1', content)
        content = re.sub(r"(\w)'?\s*:", r'\1":', content)
        content = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', content)
        return json.loads(content)

    def get_cell_indicator(self, i, j):
        cell_members = self.get_cell_members(i, j)
        if not cell_members:
            return None
        key = cell_members['key']
        indicator = INDICATORS_REGISTRY[key]['class'](self.fuchia_database)
        return indicator

    def get_cell_parameters(self, i, j):
        cell_members = self.get_cell_members(i, j)
        if not cell_members:
            return None
        parameters = cell_members
        parameters.pop('key')
        return parameters

    def get_cell_parameters_key(self, i, j):
        params = self.get_cell_parameters(i, j)
        if params is None:
            return None
        gender = params.get('gender', None)
        age_min = params.get('age_min', None)
        age_max = params.get('age_max', None)
        age_ns = params.get('age_is_null', None)
        a = utils.get_gender_str(gender)
        b = utils.get_age_range_str(age_min, age_max, age_ns)
        if a is None and b is None:
            return "Tous les patients"
        return ' '.join([i for i in [a, b] if i is not None])

    def get_cell_value(self, start_date, end_date, i, j):
        indicator = self.get_cell_indicator(i, j)
        kwargs = self.get_cell_parameters(i, j)
        if not indicator:
            return None
        kwargs['start_date'] = start_date
        if isinstance(indicator, PatientIndicator) and indicator.under_arv():
            arv = self._arv_started.get_filtered_by_category(
                end_date,
                **kwargs
            )
            kwargs['post_filter_index'] = arv.index
        value = indicator.get_value(end_date, **kwargs)
        return value

    def get_cell_patient_codes(self, start_date, end_date, i, j):
        indicator = self.get_cell_indicator(i, j)
        kwargs = self.get_cell_parameters(i, j)
        if not indicator:
            return None
        kwargs['start_date'] = start_date
        if isinstance(indicator, PatientIndicator) and indicator.under_arv():
            arv = self._arv_started.get_filtered_by_category(
                end_date,
                **kwargs
            )
            kwargs['post_filter_index'] = arv.index
        patients = indicator.get_filtered_by_category(end_date, **kwargs)
        return patients['patient_code']

    def get_cell_values(self, start_date, end_date):
        self.last_values = OrderedDict()
        self.last_template_values = {}
        matrix = np.empty((self.get_row_number(), self.get_column_number()), dtype=object)
        matrix[:] = np.NAN
        profile = {}
        total = 0
        progress = 0
        step = 10
        curr = 0
        import time
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                t = time.time()
                indicator = self.get_cell_indicator(i, j)
                matrix[i, j] = self.get_cell_value(start_date, end_date, i, j)
                if indicator is not None:
                    self.last_template_values[(i, j)] = matrix[i, j]
                    if isinstance(indicator, PatientIndicator):
                        params_key = self.get_cell_parameters_key(i, j)
                        patient_codes = self.get_cell_patient_codes(
                            start_date, end_date,
                            i, j
                        )
                        i_k = indicator.get_key()
                        if i_k not in self.last_values:
                            self.last_values[i_k] = OrderedDict()
                        self.last_values[i_k][params_key] = patient_codes
                tt = time.time() - t
                if indicator not in profile:
                    profile[indicator] = 0
                profile[indicator] += tt
                total += tt
                curr += 1
                if curr == step:
                    progress += step
                    curr = 1
                    self.update_progress.emit(progress)
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(profile)
        print("Total : {:2f}".format(total))
        return matrix

    def set_run_params(self, report_widget, start_date, end_date):
        self._report_widget = report_widget
        self._start_date = start_date
        self._end_date = end_date

    def run(self):
        try:
            b1 = self._report_widget is not None
            b2 = self._start_date is not None
            b3 = self._end_date is not None
            b = b1 and b2 and b3
            if not b:
                return
            values = self.get_cell_values(
                self._start_date,
                self._end_date
            )
            self._report_widget.set_values(values)
        except:
            excType, excValue, tracebackobj = sys.exc_info()
            tb_list = traceback.format_exception(excType,
                                                 excValue,
                                                 tracebackobj)
            tb_str = ''.join(tb_list)
            self.error.emit(tb_str)

    def get_column_number(self):
        raise NotImplementedError()

    def get_row_number(self):
        raise NotImplementedError()

    def get_merged_cell_ranges(self):
        """
        :return: A list containing the ranges of merged cells. A range is
        composed with two couples, describing the up left cell and the down
        right cell. e.g. ((1, 1), (1, 2)).
        """
        return []

    def get_cell_style(self, i, j):
        """
        :return: If a style is available for a given cell, return a dict,
        with style information about font, fill and stroke.
        """
        return None

    def get_column_width(self, j):
        return None

    def get_row_height(self, i):
        return None

    def export_to_excel(self, destination_path):
        raise NotImplementedError()
