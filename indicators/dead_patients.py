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

    def get_filtered_patients_dataframe(self, limit_date, start_date=None,
                                        gender=None, age_min=None,
                                        age_max=None, age_is_null=False,
                                        include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        return patients[is_dead & is_dead_before_limit]


class DeadPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that compute the number of patients who died during the given
    period (between start_date and limit_date).
    """

    @classmethod
    def get_key(cls):
        return "DEAD_DURING_PERIOD"

    def get_filtered_patients_dataframe(self, limit_date, start_date=None,
                                        gender=None, age_min=None,
                                        age_max=None, age_is_null=False,
                                        include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates
        )
        is_dead = pd.notnull(patients['dead'])
        is_dead_before_limit = patients['dead'] <= limit_date
        is_dead_after_start = patients['dead'] >= start_date
        return patients[is_dead & is_dead_before_limit & is_dead_after_start]
