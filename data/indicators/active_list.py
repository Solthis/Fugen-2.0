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
from data.indicators.arv_started_patients import ArvStartedPatients
from data.indicators.arv_stopped import ArvStopped
from data.indicators.dead_patients import DeadPatients
from data.indicators.lost_patients import LostPatients
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.transferred_patients import TransferredPatients
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ActiveList(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ACTIVE_LIST"

    @classmethod
    def get_display_label(cls):
        return "File active"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        arv_started = ArvStartedPatients(self.fuchia_database)
        dead = DeadPatients(self.fuchia_database)
        transferred = TransferredPatients(self.fuchia_database)
        lost = LostPatients(self.fuchia_database)
        arv_stopped = ArvStopped(self.fuchia_database)
        al = (arv_started & ~dead & ~transferred & ~lost & ~arv_stopped)
        return al.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None


class PreviousActiveList(ActiveList):

    @classmethod
    def get_key(cls):
        return "PREVIOUS_ACTIVE_LIST"

    @classmethod
    def get_display_label(cls):
        return "File active précédente"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        return super(PreviousActiveList, self).filter_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )
