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

import constants
from data.indicators.followed_patients import FollowedPatients


class CtxEligiblePatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "CTX_ELIGIBLE"

    @classmethod
    def get_display_label(cls):
        return "Eligibles au Cotrimoxazole"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        followed = FollowedPatients(
            self.fuchia_database
        ).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
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
        visits = visits[visits['patient_id'].isin(followed.index)]
        cd4 = visits['cd4'] <= 500
        oms = visits['stade_oms'] >= 2
        visits = visits[cd4 | oms]
        patient_ids = visits['patient_id'].unique()
        return followed.loc[patient_ids], None


class UnderCtxPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "UNDER_CTX"

    @classmethod
    def get_display_label(cls):
        return "Sous Cotrimoxazole"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        followed = FollowedPatients(
            self.fuchia_database
        ).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = visits[visits['next_visit_date'] >= start_date]
        visits = visits[visits['patient_id'].isin(followed.index)]
        visit_drugs = self.filter_visit_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visit_drugs = visit_drugs[visit_drugs['visit_id'].isin(visits.index)]
        visit_drugs = visit_drugs[visit_drugs['drug_id'].isin(constants.CTX)]
        visit_drugs = visit_drugs[
            visit_drugs['prescription_value'].isin(constants.DRUG_RECEIVED)
        ]
        visit_ids = visit_drugs['visit_id'].unique()
        visits = visits.loc[visit_ids]
        return followed.loc[visits['patient_id'].unique()], None
