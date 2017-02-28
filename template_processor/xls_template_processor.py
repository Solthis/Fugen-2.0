# coding: utf-8

from openpyxl import load_workbook
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
