# coding: utf-8

from indicators.patient_indicator import PatientIndicator
import constants


class TbVihPositiveDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE_DURING_PERIOD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        min_visit = visits.groupby('patient_id')['visit_date'].min()
        c1 = min_visit >= start_date
        c2 = min_visit <= limit_date
        min_visit = min_visit[c1 & c2]
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        patients = patients[patients['entry_mode'].isin(constants.TB_ENTRY)]
        inter = min_visit.index.intersection(patients.index)
        return patients.loc[inter], None
