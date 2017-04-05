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

from data.indicators.active_list import ActiveList


class ArvRepartition:
    """
    Compute the repartition of ARV treatments.
    """

    def __init__(self, fuchia_database):
        self.fuchia_database = fuchia_database

    def get_active_list_repartition(self, limit_date, start_date,
                                    include_null_dates=None):
        active_list = ActiveList(
            self.fuchia_database
        )
        patients = active_list.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visits = active_list.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = visits[pd.notnull(visits['arv_received'])]
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        last_visits = last_visits.loc[patients.index]
        # Patient drugs
        diff = patients.index.difference(
            visits.loc[last_visits]['patient_id']
        )
        patients = patients.loc[diff]['arv_drugs']
        patients = patients.value_counts()
        drugs = visits.loc[last_visits].groupby('arv_received')['patient_id'].count()
        drugs.loc[patients.index] = drugs + patients
        return drugs.sort_values(ascending=False)

    def get_prescriptions_repartition(self, limit_date, start_date,
                                      include_null_dates=None):
        active_list = ActiveList(
            self.fuchia_database
        )
        visits = active_list.filter_visits_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        drugs = visits.loc[last_visits].groupby('arv_received')['patient_id'].count()
        return drugs.sort_values(ascending=False)


