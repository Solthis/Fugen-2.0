# coding: utf-8


class BaseTemplateProcessor:
    """
    Abstract base class for report template processing.
    """

    def __init__(self, template_path):
        self.template_path = template_path

    def get_indicator_for_cell(self, i, j):
        raise NotImplementedError()

    def get_parameters_for_cell(self, i, j):
        raise NotImplementedError()

    def get_cell_value(self, start_date, end_date, i, j):
        raise NotImplementedError()

    def get_cell_values(self, start_date, end_date):
        raise NotImplementedError()

    def get_column_number(self):
        raise NotImplementedError()

    def get_row_number(self):
        raise NotImplementedError()
