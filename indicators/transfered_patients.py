# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator


class TransferredPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who are transferred
    (or decentralized) at a given date.
    """

    @classmethod
    def get_key(cls):
        return "TRANSFERRED"

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
        transferred_filter = pd.notnull(patients['transferred'])
        decentralized_filter = pd.notnull(patients['decentralized'])
        return patients[transferred_filter | decentralized_filter]


class TransferredPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that computes the number of patients who had been transferred
    during the given period (between start_date and limit_date).
    """

    @classmethod
    def get_key(cls):
        return "TRANSFERRED_DURING_PERIOD"

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
        transferred_filter = pd.notnull(patients['transferred'])
        transferred_filter &= patients['transferred'] <= limit_date
        transferred_filter &= patients['transferred'] >= start_date
        decentralized_filter = pd.notnull(patients['decentralized'])
        decentralized_filter &= patients['decentralized'] <= limit_date
        decentralized_filter &= patients['decentralized'] >= start_date
        return patients[transferred_filter | decentralized_filter]
