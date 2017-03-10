# coding: utf-8

import pandas as pd
from dateutil.relativedelta import relativedelta

from indicators.patient_indicator import PatientIndicator
from indicators.lost_patients import LostPatients
from indicators.arv_started_patients import ArvStartedPatients
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class LostBackPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "LOST_BACK"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        lost_prev = LostPatients(self.fuchia_database)
        arv_started = ArvStartedPatients(self.fuchia_database)
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        i = (lost_prev & arv_started)
        prev_lost_patients = i.filter_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )[0]
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        c1 = (visits['visit_date'] >= start_date)
        c2 = (visits['visit_date'] <= limit_date)
        visits = visits[c1 & c2]
        seen_id = pd.Index(visits['patient_id'].unique())
        n_index = prev_lost_patients.index.intersection(seen_id)
        return prev_lost_patients.loc[n_index], None


class ArvLostBackPatients(LostBackPatients):

    def under_arv(self):
            return True

    @classmethod
    def get_key(cls):
        return "ARV_LOST_BACK"
