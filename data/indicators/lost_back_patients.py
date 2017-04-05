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
from dateutil.relativedelta import relativedelta

from data.indicators.patient_indicator import PatientIndicator
from data.indicators.lost_patients import LostPatients
from data.indicators.arv_started_patients import ArvStartedPatients
from data.indicators.dead_patients import ArvDeadPatientsDuringPeriod
from data.indicators.transferred_patients import ArvTransferredPatientsDuringPeriod
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ArvLostBackPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_LOST_BACK"

    @classmethod
    def get_display_label(cls):
        return "Perdus de vue de retour dans le TARV"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        lost_prev = LostPatients(self.fuchia_database)
        arv_started = ArvStartedPatients(self.fuchia_database)
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        i = (lost_prev & arv_started)
        prev_lost_patients = i.get_filtered_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        c1 = (visits['visit_date'] >= start_date)
        c2 = (visits['visit_date'] <= limit_date)
        visits = visits[c1 & c2]
        seen_id = pd.Index(visits['patient_id'].unique())
        # Arv dead during the period must be re-included
        arv_dead = ArvDeadPatientsDuringPeriod(self.fuchia_database)
        dead = arv_dead.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        seen_id = seen_id.union(dead.index)
        # Transferred during the period must be re-included
        arv_trans = ArvTransferredPatientsDuringPeriod(self.fuchia_database)
        trans = arv_trans.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )

        seen_id = seen_id.union(trans.index)
        n_index = prev_lost_patients.index.intersection(seen_id)
        return prev_lost_patients.loc[n_index], None
