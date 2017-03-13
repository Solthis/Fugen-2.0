# coding: utf-8

import constants
from data.indicators.patient_indicator import PatientIndicator


class IncomingTransferPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that compute the number of patients already under ARV who were
    transferred from another center during the given period
    (between start_date and limit_date).
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "INCOMING_TRANSFER_DURING_PERIOD"

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
        patient_drugs = self.filter_patient_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        f_visit = visits.groupby('patient_id')['visit_date'].min()
        included = f_visit[(f_visit >= start_date) & (f_visit <= limit_date)]
        t = patient_drugs[patient_drugs['patient_id'].isin(included.index)]
        t = t['patient_id'].unique()
        return patients.loc[t], None


class ArvIncomingTransferPatientsDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_INCOMING_TRANSFER_DURING_PERIOD"

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
        patient_drugs = self.filter_patient_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        f_visit = visits.groupby('patient_id')['visit_date'].min()
        included = f_visit[(f_visit >= start_date) & (f_visit <= limit_date)]
        t = patient_drugs[patient_drugs['patient_id'].isin(included.index)]
        t = t[~t['drug_id'].isin(constants.EXCLUDED_DRUGS)]
        t = t['patient_id'].unique()
        # CASE WHEN TRANSFERRED BUT CAME BACK
        # TODO if case seen
        return patients.loc[t], None
