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

from data.indicators.active_list import ActiveList


class UnderTbTreatmentPatients(PatientIndicator):
    """
    Patients who are under a tb treatment during a given period.
    """

    @classmethod
    def get_key(cls):
        return "UNDER_TB_TREATMENT"

    @classmethod
    def get_display_label(cls):
        return "Sous traitement TB"

    def under_arv(self):
        return False

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits_tb = self.fuchia_database.visit_tb_dataframe
        c1 = visits_tb['treatment_start'] <= limit_date
        c2 = visits_tb['treatment_to'] >= limit_date
        visits_tb = visits_tb[c1 & c2]
        ids = pd.Index(visits_tb['patient_id'].unique())
        tb_index = patients.index.intersection(ids)
        return patients.loc[tb_index], None


class TbTreatmentStartedDuringPeriod(PatientIndicator):
    """
    Patients who started a tb treatment during a given period.
    """

    @classmethod
    def get_key(cls):
        return "TB_TREATMENT_STARTED"

    @classmethod
    def get_display_label(cls):
        return "Traitement TB démarré"

    def under_arv(self):
        return False

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        active_list = ActiveList(
            self.fuchia_database
        ).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visits_tb = self.fuchia_database.visit_tb_dataframe
        c1 = visits_tb['treatment_start'] >= start_date
        c2 = visits_tb['treatment_start'] <= limit_date
        visits_tb = visits_tb[c1 & c2]
        ids = pd.Index(visits_tb['patient_id'].unique())
        tb_index = active_list.index.intersection(ids)
        return active_list.loc[tb_index], None
