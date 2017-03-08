# coding: utf-8

import numpy as np

from template_processor.base_template_processor import BaseTemplateProcessor


class ArrayTemplateProcessor(BaseTemplateProcessor):

    def __init__(self, array, fuchia_database):
        super(ArrayTemplateProcessor, self).__init__(fuchia_database)
        self.array = array

    def get_row_number(self):
        if isinstance(self.array, np.ndarray):
            return self.array.shape[0]
        return len(self.array)

    def get_column_number(self):
        if isinstance(self.array, np.ndarray):
            return self.array.shape[1]
        if len(self.array) == 0:
            return 0
        return len(self.array)

    def get_cell_content(self, i, j):
        if isinstance(self.array, np.ndarray):
            return self.array[i, j]
        return self.array[i][j]
