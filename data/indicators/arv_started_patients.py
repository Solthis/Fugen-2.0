# coding: utf-8

import pandas as pd

from data.indicators.patient_indicator import PatientIndicator
import constants


class ArvStartedPatients(PatientIndicator):
    """
    Indicator that computes the number of patients who started an ARV
    treatment, whether their are still followed or not.
    """

    def under_arv(self):
        return False

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
        filter3 = visit_drugs['prescription_value'].isin(constants.DRUG_RECEIVED)
        df2 = visit_drugs[filter2 & filter3]
        df3 = visits.loc[df2['visit_id'].unique()]
        patient_ids = pd.concat(
            [df1['patient_id'], df3['patient_id']]
        ).unique()
        return patients.loc[patient_ids], None


class ArvStartedDuringPeriod(PatientIndicator):
    """
    Indicator that computes the number of patients who started an ARV
    treatment during the given period, in the given center (i.e. not incoming
    transfer).
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_STARTED_DURING_PERIOD"

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
        filter3 = visit_drugs['prescription_value'].isin(constants.DRUG_RECEIVED)
        df2 = visit_drugs[filter2 & filter3]
        df3 = visits[visits['id'].isin(df2['visit_id'])]
        s1 = df1.groupby('patient_id')['beginning'].min()
        s2 = df3.groupby('patient_id')['visit_date'].min()
        a = s1[s1 <= start_date]
        b = s2[(s2 >= start_date) & (s2 <= limit_date)]
        diff = b.index.difference(a.index)
        if len(diff) == 0:
            return patients[:0], None
        s = b.loc[diff]
        if len(s.index) == 0:
            return patients[:0], None
        return patients.loc[s.index], None
