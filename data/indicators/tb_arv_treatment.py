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


from data.indicators.active_list import ActiveList
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.tb_treatment import UnderTbTreatmentPatients


class UnderTbTreatmentAndArvPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_ARV_TREATMENT"

    @classmethod
    def get_display_label(cls):
        return "Sous traitement TB et TARV"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        tb_treatment = UnderTbTreatmentPatients(self.fuchia_database)
        active_list = ActiveList(self.fuchia_database)
        arv_and_tb_treatment = (tb_treatment & active_list)
        return arv_and_tb_treatment.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
