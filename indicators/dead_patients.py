# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator


class DeadPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who are dead at a
    given date.
    """

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
        return patients[pd.notnull(patients['dead'])]


class DeadPatientsAtPeriod(DeadPatients):
    """
    Indicator that compute the number of patients who died at the given
    period.
    """

    pass
