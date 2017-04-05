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


class TransferredPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who are transferred
    (or decentralized) at a given date.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TRANSFERRED_ALL"

    @classmethod
    def get_display_label(cls):
        return "Transférés (tous jusqu'à la fin de la période)"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        transferred_filter = pd.notnull(patients['transferred'])
        transferred_filter &= patients['transferred'] <= limit_date
        decentralized_filter = pd.notnull(patients['decentralized'])
        decentralized_filter &= patients['decentralized'] <= limit_date
        transferred = patients[transferred_filter | decentralized_filter]
        transferred = transferred.groupby('id')[
            ('transferred', 'decentralized')
        ].max().max(axis=1)
        # CASE WHEN TRANSFERRED BUT CAME BACK
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = visits.groupby('patient_id')['visit_date'].max()
        visits = visits.loc[visits.index.intersection(transferred.index)]
        transferred = transferred[transferred >= visits]
        return patients.loc[transferred.index], None


class TransferredPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that computes the number of patients who had been transferred
    during the given period (between start_date and limit_date).
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TRANSFERRED"

    @classmethod
    def get_display_label(cls):
        return "Transférés"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        transferred_filter = pd.notnull(patients['transferred'])
        transferred_filter &= patients['transferred'] <= limit_date
        transferred_filter &= patients['transferred'] >= start_date
        decentralized_filter = pd.notnull(patients['decentralized'])
        decentralized_filter &= patients['decentralized'] <= limit_date
        decentralized_filter &= patients['decentralized'] >= start_date
        return patients[transferred_filter | decentralized_filter], None


class ArvTransferredPatientsDuringPeriod(TransferredPatientsDuringPeriod):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_TRANSFERRED"

    @classmethod
    def get_display_label(cls):
        return "Transférés sous ARV"
