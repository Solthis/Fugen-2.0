# coding: utf-8

import re

import numpy as np


class BaseTemplateProcessor:
    """
    Abstract base class for report template processing.
    """

    def __init__(self, template_path):
        self.template_path = template_path

    def get_cell_content(self, i, j):
        raise NotImplementedError()

    def get_cell_members(self, i, j):
        regex = "^\{(.+?)\}$"
        res = re.findall(regex, self.get_cell_content(i, j))
        return res[0].split(";")

    def get_cell_indicator(self, i, j):
        pass

    def get_cell_parameters(self, i, j):
        pass

    def get_cell_value(self, start_date, end_date, i, j):
        raise NotImplementedError()

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
