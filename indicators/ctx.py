# coding: utf-8

from indicators.patient_indicator import PatientIndicator
from indicators.followed_patients import FollowedPatients
import constants


class CtxEligiblePatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "CTX_ELIGIBLE"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        followed = FollowedPatients(
            self.fuchia_database
        ).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
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
        visits = visits[visits['patient_id'].isin(followed.index)]
        cd4 = visits['cd4'] <= 500
        oms = visits['stade_oms'] >= 2
        visits = visits[cd4 | oms]
        patient_ids = visits['patient_id'].unique()
        return followed.loc[patient_ids], None


class UnderCtxPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "UNDER_CTX"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        followed = FollowedPatients(
            self.fuchia_database
        ).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = visits[visits['next_visit_date'] >= start_date]
        visits = visits[visits['patient_id'].isin(followed.index)]
        visit_drugs = self.filter_visit_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visit_drugs = visit_drugs[visit_drugs['visit_id'].isin(visits.index)]
        visit_drugs = visit_drugs[visit_drugs['drug_id'].isin(constants.CTX)]
        visit_ids = visit_drugs['visit_id'].unique()
        visits = visits.loc[visit_ids]
        return followed.loc[visits['patient_id'].unique()], None
