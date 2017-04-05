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


import pandas as pd

from data.indicators.patient_indicator import PatientIndicator


class DeadPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who are dead at a
    given date.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "DEAD_ALL"

    @classmethod
    def get_display_label(cls):
        return "Décédés (tous jusqu'à la fin de la période)"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        return patients[is_dead & is_dead_before_limit], None


class DeadPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that compute the number of patients who died during the given
    period (between start_date and limit_date).
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "DEAD"

    @classmethod
    def get_display_label(cls):
        return "Décédés"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        is_dead_after_start = patients['dead'] >= start_date
        r = patients[is_dead & is_dead_before_limit & is_dead_after_start]
        return r, None


class ArvDeadPatientsDuringPeriod(DeadPatientsDuringPeriod):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_DEAD"

    @classmethod
    def get_display_label(cls):
        return "Sous TARV décédés"
