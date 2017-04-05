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


from data.indicators.patient_indicator import PatientIndicator


class IncludedPatients(PatientIndicator):
    """
    Basic indicator, computes the number of patients that had been included
    in the follow up, whether there are under arv, died, lost...
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "INCLUDED_ALL"

    @classmethod
    def get_display_label(cls):
        return "Patients inscrits dans la base"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        return self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        ), None
