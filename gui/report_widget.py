# coding: utf-8

import threading

from PySide.QtCore import *
from PySide.QtGui import *
import pandas as pd


class ReportWidget(QWidget):

    def __init__(self, template_processor=None, parent=None):
        super(ReportWidget, self).__init__(parent=parent)
        self._template_processor = None
        # Init table widget
        self.setLayout(QVBoxLayout())
        self.table_widget = QTableWidget(self)
        self.layout().addWidget(self.table_widget)
        self.template_processor = template_processor

    @property
    def template_processor(self):
        return self._template_processor

    @template_processor.setter
    def template_processor(self, value):
        self._template_processor = value
        self.table_widget.clearContents()
        if self._template_processor is not None:
            self.table_widget.setRowCount(
                self.template_processor.get_row_number()
            )
            self.table_widget.setColumnCount(
                self.template_processor.get_column_number()
            )

    def compute_values(self, start_date, end_date):
        def func():
            values = self.template_processor.get_cell_values(
                start_date,
                end_date
            )
            self.set_values(values)
        thread = threading.Thread(target=func)
        thread.start()

    def set_values(self, values):
        n_row = values.shape[0]
        n_col = values.shape[1]
        for i in range(n_row):
            for j in range(n_col):
                v = values[i, j]
                if pd.isnull(v):
                    v = self.template_processor.get_cell_content(i, j)
                    v = v if pd.notnull(v) else ""
                item = QTableWidgetItem(str(v))
                self.table_widget.setItem(i, j, item)
