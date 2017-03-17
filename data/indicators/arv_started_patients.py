# coding: utf-8

import pandas as pd

from data.indicators.patient_indicator import PatientIndicator


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

    @classmethod
    def get_display_label(cls):
        return "Traitement ARV démarré (Toutes périodes confondues)"

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
        df1 = patients[pd.notnull(patients['arv_drugs'])]
        df2 = visits[pd.notnull(visits['arv_received'])]
        patient_ids = df1.index.union(pd.Index(df2['patient_id'].unique()))
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

    @classmethod
    def get_display_label(cls):
        return "Traitement ARV démarré"

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
        df1 = patients[pd.notnull(patients['arv_drugs'])]
        df2 = visits[pd.notnull(visits['arv_received'])]
        s2 = df2.groupby('patient_id')['visit_date'].min()
        b = s2[(s2 >= start_date) & (s2 <= limit_date)]
        diff = b.index.difference(df1.index)
        if len(diff) == 0:
            return patients[:0], None
        s = b.loc[diff]
        if len(s.index) == 0:
            return patients[:0], None
        return patients.loc[s.index], None
