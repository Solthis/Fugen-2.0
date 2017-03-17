# coding: utf-8

from PySide.QtCore import *
from PySide.QtGui import *
import pandas as pd

import utils


class ReportWidget(QWidget):

    report_processed = Signal()
    processing_error = Signal()

    def __init__(self, template_processor=None, parent=None):
        super(ReportWidget, self).__init__(parent=parent)
        self._template_processor = None
        l = QVBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        self.setLayout(l)
        self.table_widget = QTableWidget(self)
        self.table_widget.setFrameShape(QFrame.NoFrame)
        self.table_widget.setWordWrap(True)
        self.table_widget.setHorizontalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )
        self.table_widget.setVerticalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )
        self.layout().addWidget(self.table_widget)
        self.template_processor = template_processor
        self.worker = None

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
            self.template_processor.error.connect(self.error)

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
                self.set_cell_style(i, j)

    def set_cell_style(self, i, j):
        style = self.template_processor.get_cell_style(i, j)
        if not style:
            return
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
        self.template_processor.set_run_params(
            self,
            start_date,
            end_date
        )
        self.template_processor.start()

    def cell_count(self):
        column_count = self.template_processor.get_column_number()
        row_count = self.template_processor.get_row_number()
        return column_count * row_count

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
        self.report_processed.emit()

    def error(self, stacktrace):
        t = "Une erreur est survenue pendant le calcul du rapport"
        m = "Assurez vous d'avoir bien configuré l'outil et le template du" \
            " rapport à générer, puis redémarrez le logiciel Si l'erreur " \
            "persiste, contactez Solthis."
        msg_box = utils.getCriticalMessageBox(t, m, stacktrace)
        msg_box.exec_()
        self.processing_error.emit()
