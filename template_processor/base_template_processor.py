# coding: utf-8

import re
import json

import numpy as np

from indicators import INDICATORS_REGISTRY


class BaseTemplateProcessor:
    """
    Abstract base class for report template processing.
    """

    def __init__(self, template_path, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        self.template_path = template_path
        self.patients_dataframe = patients_dataframe
        self.visits_dataframe = visits_dataframe
        self.patient_drugs_dataframe = patient_drugs_dataframe
        self.visit_drugs_dataframe = visit_drugs_dataframe
        self._indicators = {}

    def get_cell_content(self, i, j):
        raise NotImplementedError()

    def get_cell_members(self, i, j):
        regex = "^\{(.+?)\}$"
        content = self.get_cell_content(i, j)
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
        indicator = INDICATORS_REGISTRY[key](
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        self._indicators[key] = indicator
        return indicator

    def get_cell_parameters(self, i, j):
        parameters = self.get_cell_members(i, j)
        parameters.pop('key')
        return parameters

    def get_cell_value(self, start_date, end_date, i, j):
        indicator = self.get_cell_indicator(i, j)
        kwargs = self.get_cell_parameters(i, j)
        kwargs['start_date'] = start_date
        value = indicator.get_value(end_date, **kwargs)
        return value

    def get_cell_values(self, start_date, end_date):
        matrix = np.empty((self.get_row_number(), self.get_column_number()))
        matrix[:] = np.NAN
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                matrix[i, j] = self.get_cell_value(start_date, end_date, i, j)
        return matrix

    def get_column_number(self):
        raise NotImplementedError()

    def get_row_number(self):
        raise NotImplementedError()
