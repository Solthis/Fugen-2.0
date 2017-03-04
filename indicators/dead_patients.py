# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator


class DeadPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who are dead at a
    given date.
    """

    @classmethod
    def get_key(cls):
        return "DEAD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        return patients[is_dead & is_dead_before_limit], None


class DeadPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that compute the number of patients who died during the given
    period (between start_date and limit_date).
    """

    @classmethod
    def get_key(cls):
        return "DEAD_DURING_PERIOD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        is_dead_after_start = patients['dead'] >= start_date
        r = patients[is_dead & is_dead_before_limit & is_dead_after_start]
        return r, None
