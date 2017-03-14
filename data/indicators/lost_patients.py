# coding: utf-8

from data.indicators.arv_stopped import ArvStopped
from data.indicators.dead_patients import DeadPatients
from data.indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator
from pandas.tseries.offsets import *

import constants
from data.indicators.transferred_patients import TransferredPatients


class LostPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "LOST"

    @classmethod
    def get_display_label(cls):
        return "Perdus de vue (toutes périodes confondues)"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        last_next = visits.groupby('patient_id')[
            ('next_visit_date', 'visit_date')
        ].max().max(axis=1)
        lost_date = last_next + DateOffset(months=constants.PDV_MONTHS_DELAY)
        lost = lost_date[lost_date <= limit_date]
        dead = DeadPatients(self.fuchia_database)
        transferred = TransferredPatients(self.fuchia_database)
        arv_stopped = ArvStopped(self.fuchia_database)
        exclude = (dead | transferred | arv_stopped).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        lost = lost.loc[lost.index.difference(exclude.index)]
        return patients.loc[lost.index], lost


class LostDuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = LostPatients(fuchia_database)
        super(LostDuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "LOST_DURING_PERIOD"

    @classmethod
    def get_display_label(cls):
        return "Perdus de vue"


class ArvLostDuringPeriod(LostDuringPeriod):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST_DURING_PERIOD"

    @classmethod
    def get_display_label(cls):
        return "Perdus de vue sous TARV"


class ArvLost(LostPatients):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST"

    @classmethod
    def get_display_label(cls):
        return "Perdus de vue sous TARV (toutes périodes confondues)"
