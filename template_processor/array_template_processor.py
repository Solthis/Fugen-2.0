# coding: utf-8

# Copyright 2017 Solthis.
#
# This file is part of Fugen 2.0.
#
# Fugen 2.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fugen 2.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fugen 2.0. If not, see <http://www.gnu.org/licenses/>.


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
