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


from data.indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator

from data.indicators.followed_patients import FollowedPatients


class TbDiagnosisPatients(PatientIndicator):
    """
    Patients who had at least one tb diagnosis since they where included
    in the follow up.
    """

    @classmethod
    def get_key(cls):
        return "TB_DIAGNOSIS_ALL"

    def under_arv(self):
        return False

    @classmethod
    def get_display_label(cls):
        return "TB diagnostiquée (tous jusqu'à la fin de la période)"

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
        visits = visits[visits['tb_diagnosis']]
        visits = visits.groupby('patient_id')['visit_date'].max()
        f_index = followed.index.intersection(visits.index)
        return followed.loc[f_index], visits.loc[f_index]


class TbDiagnosisDuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = TbDiagnosisPatients(fuchia_database)
        super(TbDiagnosisDuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "TB_DIAGNOSIS"

    @classmethod
    def get_display_label(cls):
        return "TB diagnostiquée"
