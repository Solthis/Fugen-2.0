# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator
import constants


class ArvStartedPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who started an ARV
    treatment, whether their are still followed or not.
    """

    @classmethod
    def get_key(cls):
        return "ARV_STARTED"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        patient_drugs = self.filter_patient_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visit_drugs = self.filter_visit_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        filter1 = ~patient_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        df1 = patient_drugs[filter1]
        filter2 = ~visit_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        df2 = visit_drugs[filter2]
        df3 = visits[visits['id'].isin(df2['visit_id'])]
        patient_ids = pd.concat(
            [df1['patient_id'], df3['patient_id']]
        ).unique()
        return patients[patients['id'].isin(patient_ids)]
