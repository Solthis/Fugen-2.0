# coding: utf-8

from indicators.patient_indicator import PatientIndicator
from indicators.followed_patients import FollowedPatients


class CtxEligiblePatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "CTX_ELIGIBLE"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        followed = FollowedPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
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
        visits = visits[visits['patient_id'].isin(followed.index)]
        c1 = (visits['visit_date'] >= start_date)
        c2 = (visits['visit_date'] <= limit_date)
        visits = visits[c1 & c2]
        cd4 = visits['cd4'] <= 500
        oms = visits['stade_oms'] >= 2
        visits = visits[cd4 | oms]
        patient_ids = visits['patient_id'].unique()
        return followed.loc[patient_ids], None
