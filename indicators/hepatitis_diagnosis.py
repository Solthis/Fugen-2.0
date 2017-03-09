# coding: utf-8

from indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator
from indicators.followed_patients import FollowedPatients


class HepatitisBDiagnosisPatients(PatientIndicator):
    """
    Patients who had at least one hepatitis b diagnosis since they where
    included in the follow up.
    """

    @classmethod
    def get_key(cls):
        return "HEPATITIS_B_DIAGNOSIS"

    def under_arv(self):
        return False

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
        visits = visits[visits['hepatitis_b_diagnosis']]
        visits = visits.groupby('patient_id')['visit_date'].max()
        f_index = followed.index.intersection(visits.index)
        return followed.loc[f_index], visits.loc[f_index]


class HepatitisBDiagnosisDuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = HepatitisBDiagnosisPatients(fuchia_database)
        super(HepatitisBDiagnosisDuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "HEPATITIS_B_DIAGNOSIS_DURING_PERIOD"