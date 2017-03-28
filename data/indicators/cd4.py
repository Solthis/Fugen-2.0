# coding: utf-8

import pandas as pd

from data.indicators.patient_indicator import PatientIndicator
from data.indicators.arv_started_patients import ArvStartedDuringPeriod


class HadCd4Patients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4_ALL"

    @classmethod
    def get_display_label(cls):
        return "Comptage CD4 reçu (tous jusqu'à la fin de la période)"

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
        cd4 = pd.Index(visits['patient_id'].unique())
        return patients.loc[cd4], None


class HadCd4DuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4"

    @classmethod
    def get_display_label(cls):
        return "Comptage CD4 reçu"

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
        c1 = visits['visit_date'] >= start_date
        c2 = visits['visit_date'] <= limit_date
        visits = visits[c1 & c2]
        cd4 = pd.Index(visits['patient_id'].unique())
        return patients.loc[cd4], None


class HadCd4Inf200DuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4_INF_200"

    @classmethod
    def get_display_label(cls):
        return "CD4 < 200 cells/" + u"\u00B5" + "L"

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
        c1 = visits['visit_date'] >= start_date
        c2 = visits['visit_date'] <= limit_date
        visits = visits[c1 & c2]
        visits = visits[visits['cd4'] < 200]
        cd4 = pd.Index(visits['patient_id'].unique())
        return patients.loc[cd4], None


class HadCd4AtArvStartDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CD4_AT_ARV_START"

    @classmethod
    def get_display_label(cls):
        return "Comptage CD4 disponible à l'initiation du TARV"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        had_cd4 = HadCd4DuringPeriod(self.fuchia_database)
        arv_started = ArvStartedDuringPeriod(self.fuchia_database)
        return (had_cd4 & arv_started).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None


class HadCd4Inf200AtArvStartDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "CD4_INF_200_AT_ARV_START"

    @classmethod
    def get_display_label(cls):
        return "CD4 < 200 cells/" + u"\u00B5" + "L à l'initiation du TARV"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        had_cd4_inf_200 = HadCd4Inf200DuringPeriod(self.fuchia_database)
        arv_started = ArvStartedDuringPeriod(self.fuchia_database)
        return (had_cd4_inf_200 & arv_started).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
