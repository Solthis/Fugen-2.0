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
from data.indicators.arv_started_patients import ArvStartedDuringPeriod
import constants


class TbVihPositive(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE_ALL"

    @classmethod
    def get_display_label(cls):
        return "Patients TB dépisté VIH+ (tous jusqu'à la fin de la période)"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        min_visit = visits.groupby('patient_id')['visit_date'].min()
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        patients = patients[patients['entry_mode'].isin(constants.TB_ENTRY)]
        inter = min_visit.index.intersection(patients.index)
        return patients.loc[inter], min_visit.loc[inter]


class TbVihPositiveDuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = TbVihPositive(fuchia_database)
        super(TbVihPositiveDuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE"

    @classmethod
    def get_display_label(cls):
        return "Patients TB dépisté VIH+"


class TbVihPositiveArvStartedDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE_ARV_STARTED"

    @classmethod
    def get_display_label(cls):
        return "Patients TB dépisté VIH+ ayant démarré le TARV"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        tb_entry = TbVihPositive(self.fuchia_database)
        arv_started = ArvStartedDuringPeriod(self.fuchia_database)
        return (tb_entry & arv_started).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
