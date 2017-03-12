# coding: utf-8

from indicators.patient_indicator import PatientIndicator
import constants


class ArvStopped(PatientIndicator):
    """
    Indicator that computes the number of patients who stopped the ARV
    treatment during the given period.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_STOPPED"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visit_drugs = self.filter_visit_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_at_date(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        # Arv stopped
        filter1 = ~visit_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        filter2 = visit_drugs['prescription_value'].isin(constants.DRUG_STOPPED)
        df1 = visit_drugs[filter1 & filter2]
        arv_stopped = visits.loc[df1['visit_id'].unique()]
        arv_stopped = arv_stopped.groupby('patient_id')['visit_date'].max()
        # Arv received
        filter3 = visit_drugs['prescription_value'].isin(constants.DRUG_RECEIVED)
        df2 = visit_drugs[filter1 & filter3]
        arv_received = visits.loc[df2['visit_id'].unique()]
        arv_received = arv_received.groupby('patient_id')['visit_date'].max()
        inter_idx = arv_stopped.index.intersection(arv_received.index)
        inter_a = arv_stopped.loc[inter_idx]
        inter_b = arv_received.loc[inter_idx]
        inter_stopped = inter_a[inter_a > inter_b]
        f_idx = arv_stopped.index\
            .difference(arv_received.index)\
            .union(inter_stopped.index)
        return patients.loc[f_idx], None


class ArvStoppedDuringPeriod(PatientIndicator):
    """
    Indicator that computes the number of patients who stopped the ARV
    treatment during the given period.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_STOPPED_DURING_PERIOD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visit_drugs = self.filter_visit_drugs_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_at_date(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        filter1 = ~visit_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        filter2 = visit_drugs['prescription_value'].isin(constants.DRUG_STOPPED)
        filter3 = visit_drugs['prescription_value'].isin(constants.DRUG_RECEIVED)
        df1 = visit_drugs[filter1 & filter2]
        df2 = visit_drugs[filter1 & filter3]
        df3 = visit_drugs.loc[df1.index.difference(df2.index)]
        arv_stopped = visits.loc[df3['visit_id'].unique()]
        return patients.loc[arv_stopped['patient_id'].unique()], None
