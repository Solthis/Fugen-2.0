# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator,\
    DuringPeriodIndicator
from indicators.arv_started_patients import ArvStartedDuringPeriod


class HadCd4Patients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4"

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
        visits = visits[pd.notnull(visits['cd4'])]
        last_cd4 = visits.groupby('patient_id')['visit_date'].max()
        return patients.loc[last_cd4.index], last_cd4


class HadCd4DuringPeriod(DuringPeriodIndicator):

    def __init__(self, fuchia_database):
        indicator = HadCd4Patients(fuchia_database)
        super(HadCd4DuringPeriod, self).__init__(
            indicator,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "HAD_CD4_DURING_PERIOD"


class HadCd4AtsArvStart(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4_AT_ARV_START"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        had_cd4 = HadCd4DuringPeriod(self.fuchia_database)
        arv_started = ArvStartedDuringPeriod(self.fuchia_database)
        return (had_cd4 & arv_started).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
