# coding: utf-8

import re
import json

import numpy as np
import pandas as pd
from PySide.QtCore import QThread, Signal

from indicators import INDICATORS_REGISTRY, ArvStartedPatients


class BaseTemplateProcessor(QThread):
    """
    Abstract base class for report template processing.
    """

    update_progress = Signal(int)

    def __init__(self, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        super(BaseTemplateProcessor, self).__init__()
        self.patients_dataframe = patients_dataframe
        self.visits_dataframe = visits_dataframe
        self.patient_drugs_dataframe = patient_drugs_dataframe
        self.visit_drugs_dataframe = visit_drugs_dataframe
        self._arv_started = ArvStartedPatients(
                patients_dataframe,
                visits_dataframe,
                patient_drugs_dataframe,
                visit_drugs_dataframe
        )
        self._indicators = {
            ArvStartedPatients.get_key(): self._arv_started
        }
        self._report_widget = None
        self._start_date = None
        self._end_date = None

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
        if key in self._indicators:
            return self._indicators[key]
        indicator = INDICATORS_REGISTRY[key]['class'](
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        self._indicators[key] = indicator
        return indicator

    def get_cell_parameters(self, i, j):
        cell_members = self.get_cell_members(i, j)
        if not cell_members:
            return None
        parameters = cell_members
        parameters.pop('key')
        return parameters

    def get_cell_value(self, start_date, end_date, i, j):
        indicator = self.get_cell_indicator(i, j)
        kwargs = self.get_cell_parameters(i, j)
        if not indicator:
            return None
        kwargs['start_date'] = start_date
        if indicator.under_arv():
            arv = self._arv_started.get_filtered_by_category(
                end_date,
                **kwargs
            )
            kwargs['post_filter_index'] = arv.index
        value = indicator.get_value(end_date, **kwargs)
        return value

    def get_cell_values(self, start_date, end_date):
        matrix = np.empty((self.get_row_number(), self.get_column_number()))
        matrix[:] = np.NAN
        profile = {}
        total = 0
        progress = 0
        import time
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                t = time.time()
                indicator = self.get_cell_indicator(i, j)
                matrix[i, j] = self.get_cell_value(start_date, end_date, i, j)
                tt = time.time() - t
                if indicator not in profile:
                    profile[indicator] = 0
                profile[indicator] += tt
                total += tt
                progress += 1
                self.update_progress.emit(progress)
        for k, v in profile.items():
            print("{} : {:2f}".format(k, v))
        print("Total : {:2f}".format(total))
        return matrix

    def set_run_params(self, report_widget, start_date, end_date):
        self._report_widget = report_widget
        self._start_date = start_date
        self._end_date = end_date

    def run(self):
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
