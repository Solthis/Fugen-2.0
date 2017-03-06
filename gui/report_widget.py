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
        self.table_widget.setWordWrap(True)
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
            self.set_spans()
            self.set_text_values()
            self.set_styles()
            self.set_row_heights()
            self.set_column_widths()

    def set_spans(self):
        for merge_range in self.template_processor.get_merged_cell_ranges():
            row, column = merge_range[0]
            row_span = abs(row - merge_range[1][0]) + 1
            col_span = abs(column - merge_range[1][1]) + 1
            self.table_widget.setSpan(row, column, row_span, col_span)

    def set_text_values(self):
        n_row = self.template_processor.get_row_number()
        n_col = self.template_processor.get_column_number()
        for i in range(n_row):
            for j in range(n_col):
                v = self.template_processor.get_cell_members(i, j)
                if pd.notnull(v):
                    item = QTableWidgetItem('')
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table_widget.setItem(i, j, item)
                    continue
                v = self.template_processor.get_cell_content(i, j)
                v = v if pd.notnull(v) else ""
                item = QTableWidgetItem(str(v))
                item.setFlags(Qt.ItemIsEnabled)
                self.table_widget.setItem(i, j, item)

    def set_styles(self):
        n_row = self.template_processor.get_row_number()
        n_col = self.template_processor.get_column_number()
        for i in range(n_row):
            for j in range(n_col):
                style = self.template_processor.get_cell_style(i, j)
                if not style:
                    continue
                item = self.table_widget.item(i, j)
                # Fill
                if 'fill' in style:
                    r, g, b, a = style['fill']['color']
                    color = QColor(r, g, b, a)
                    brush = QBrush(color)
                    item.setBackground(brush)
                # Alignment
                if 'alignment' in style:
                    item.setTextAlignment(style['alignment'])

    def set_column_widths(self):
        n_col = self.template_processor.get_column_number()
        for j in range(n_col):
            w = self.template_processor.get_column_width(j)
            if w is None:
                return
            self.table_widget.setColumnWidth(j, w)

    def set_row_heights(self):
        n_row = self.template_processor.get_row_number()
        for i in range(n_row):
            h = self.template_processor.get_row_height(i)
            if h is None:
                return
            self.table_widget.setRowHeight(i, h)

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
                    continue
                item = self.table_widget.item(i, j)
                item.setText(str(v))