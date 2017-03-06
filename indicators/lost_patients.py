# coding: utf-8

from pandas.tseries.offsets import *

from indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator
from indicators.dead_patients import DeadPatients
from indicators.transferred_patients import TransferredPatients
import constants


class LostPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "LOST"

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
        dead = DeadPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        transferred = TransferredPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        dead_or_transferred = (dead | transferred).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        lost = lost.loc[lost.index.difference(dead_or_transferred.index)]
        return patients.loc[lost.index], lost


class LostDuringPeriod(DuringPeriodIndicator):

    def __init__(self, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        indicator = LostPatients(
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )
        super(LostDuringPeriod, self).__init__(
            indicator,
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @classmethod
    def get_key(cls):
        return "LOST_DURING_PERIOD"


class ArvLostDuringPeriod(LostDuringPeriod):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST_DURING_PERIOD"


class ArvLost(LostPatients):

    def under_arv(self):
        return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST"
