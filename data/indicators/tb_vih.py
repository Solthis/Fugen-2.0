# coding: utf-8

from data.indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator
from data.indicators.arv_started_patients import ArvStartedDuringPeriod
import constants


class TbVihPositive(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        min_visit = visits.groupby('patient_id')['visit_date'].min()
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        patients = patients[patients['entry_mode'].isin(constants.TB_ENTRY)]
        inter = min_visit.index.intersection(patients.index)
        return patients.loc[inter], min_visit.loc[inter]


class TbVihPositiveDuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = TbVihPositive(fuchia_database)
        super(TbVihPositiveDuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE_DURING_PERIOD"


class TbVihPositiveArvStartedDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_VIH_POSITIVE_ARV_STARTED_DURING_PERIOD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        tb_entry = TbVihPositive(self.fuchia_database)
        arv_started = ArvStartedDuringPeriod(self.fuchia_database)
        return (tb_entry & arv_started).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
