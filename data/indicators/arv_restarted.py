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


from dateutil.relativedelta import relativedelta
from data.indicators.arv_stopped import ArvStopped
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.active_list import ActiveList
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ArvRestartedDuringPeriod(PatientIndicator):
    """
    Patients who stopped the treatment during the previous period, and
    started it again.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_RESTARTED"

    @classmethod
    def get_display_label(cls):
        return "Traitement repris"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        stopped_prev = ArvStopped(self.fuchia_database)
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        stopped_prev_patients = stopped_prev.get_filtered_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )
        al = ActiveList(self.fuchia_database)
        active_list = al.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        idx = stopped_prev_patients.index.intersection(active_list.index)
        return active_list.loc[idx], None
