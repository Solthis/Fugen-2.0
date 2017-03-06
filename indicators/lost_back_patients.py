# coding: utf-8

from dateutil.relativedelta import relativedelta

from indicators.patient_indicator import PatientIndicator
from indicators.lost_patients import LostDuringPeriod, LostPatients
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class LostBackPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "LOST_BACK"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        lost_prev = LostDuringPeriod(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        lost = LostPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        prev_lost_patients = lost_prev.filter_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )[0]
        lost_patients = lost.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        diff = prev_lost_patients.index.difference(lost_patients.index)
        return prev_lost_patients.loc[diff], None


class ArcLostBackPatients(LostBackPatients):

    def under_arv(self):
            return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST_BACK"
