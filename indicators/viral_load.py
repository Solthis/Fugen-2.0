# coding: utf-8

import pandas as pd
from dateutil.relativedelta import relativedelta

from indicators.patient_indicator import PatientIndicator
from indicators.arv_started_patients import ArvStartedDuringPeriod
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class HadViralLoadPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CV"

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
        visits = visits[pd.notnull(visits['viral_load'])]
        last_cv = visits.groupby('patient_id')['visit_date'].max()
        return patients.loc[last_cv.index], last_cv


class HadViralLoadInf1000Patients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CV_INF_1000"

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
        visits = visits[pd.notnull(visits['viral_load'])]
        visits = visits.sort_values(
            ['patient_id', 'visit_date'],
            ascending=[True, False]
        )
        visits = visits.groupby('patient_id').agg({
            'visit_date': 'max',
            'viral_load': 'first'
        })
        cv_inf_1000 = visits[visits['viral_load'] < 1000]
        return patients.loc[cv_inf_1000.index], cv_inf_1000['visit_date']


class HadViralLoad12Months(HadViralLoadPatients):

    @classmethod
    def get_key(cls):
        return "HAD_CV_12_MONTH"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        data = super(HadViralLoad12Months, self).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        patients = data[0]
        last_cv = data[1]
        p_start = start_date - relativedelta(months=12)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        cv_12_months = last_cv[last_cv >= p_start]
        return patients.loc[cv_12_months.index], cv_12_months


class HadViralLoad12Inf1000(HadViralLoadInf1000Patients):

    @classmethod
    def get_key(cls):
        return "HAD_CV_INF_1000_12_MONTH"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        data = super(HadViralLoad12Inf1000, self).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        patients = data[0]
        last_cv = data[1]
        p_start = start_date - relativedelta(months=12)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        cv_12_months = last_cv[last_cv >= p_start]
        return patients.loc[cv_12_months.index], cv_12_months


class HadViralLoad12MonthsArvStart(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CV_WITHIN_12_MONTH_AFTER_ARV_START"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        cv_12_months = HadViralLoad12Months(self.fuchia_database)
        cv_12_months_patients = cv_12_months.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        p_limit = limit_date - relativedelta(months=12)
        p_start = start_date - relativedelta(months=12)
        p_limit = getLastDayOfPeriod(p_limit.month, p_limit.year)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        arv_started = ArvStartedDuringPeriod(
            self.fuchia_database
        ).filter_patients_dataframe(
            p_limit,
            start_date=p_start,
            include_null_dates=include_null_dates
        )[0]
        idx = cv_12_months_patients.index.intersection(arv_started.index)
        return arv_started.loc[idx], None


class HadViralLoad12Inf1000ArvStart(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "HAD_CV_INF_1000_WITHIN_12_MONTH_AFTER_ARV_START"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        cv_12_months = HadViralLoad12Inf1000(self.fuchia_database)
        cv_12_months_patients = cv_12_months.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        p_limit = limit_date - relativedelta(months=12)
        p_start = start_date - relativedelta(months=12)
        p_limit = getLastDayOfPeriod(p_limit.month, p_limit.year)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        arv_started = ArvStartedDuringPeriod(
            self.fuchia_database
        ).filter_patients_dataframe(
            p_limit,
            start_date=p_start,
            include_null_dates=include_null_dates
        )[0]
        idx = cv_12_months_patients.index.intersection(arv_started.index)
        return arv_started.loc[idx], None
