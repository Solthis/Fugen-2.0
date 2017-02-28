# coding: utf-8

from openpyxl import load_workbook
from openpyxl.utils import coordinate_to_tuple
import pandas as pd

from template_processor.array_template_processor import ArrayTemplateProcessor


class XlsTemplateProcessor(ArrayTemplateProcessor):

    def __init__(self, xls_template_path, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        self._xls_template_path = xls_template_path
        self._workbook = load_workbook(self.xls_template_path)
        super(XlsTemplateProcessor, self).__init__(
            pd.DataFrame(self._workbook.active.values).as_matrix(),
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @property
    def xls_template_path(self):
        return self._xls_template_path

    @xls_template_path.setter
    def xls_template_path(self, value):
        self._xls_template_path = value
        self._workbook = load_workbook(self.xls_template_path)
        self.array = pd.DataFrame(self._workbook.active.values).as_matrix()

    def get_merged_cell_ranges(self):
        """
        :return: A list containing the ranges of merged cells. A range is
        composed with two couples, describing the up left cell and the down
        right cell. e.g. ((1, 1), (1, 2)).
        """
        merged_cell_ranges = self._workbook.active.merged_cell_ranges
        split = [i.split(':') for i in merged_cell_ranges]
        coordinates = [tuple([coordinate_to_tuple(i) for i in t])
                       for t in split]
        fixed = []
        # Fix indices
        for r in coordinates:
            a, b = r[0]
            c, d = r[1]
            fixed.append(((a - 1, b - 1), (c - 1, d - 1)))
        return fixed
