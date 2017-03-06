# coding: utf-8

from dateutil.relativedelta import relativedelta

from indicators.patient_indicator import PatientIndicator
from indicators.arv_started_patients import ArvStartedDuringPeriod
from indicators.active_list import ActiveList
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ArvRetentionPatients(PatientIndicator):

    def __init__(self, retention_duration, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        super(ArvRetentionPatients, self).__init__(
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )
        self.retention_duration = retention_duration

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        active_list = ActiveList(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        ).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        p_limit = limit_date - relativedelta(months=self.retention_duration)
        p_start = start_date - relativedelta(months=self.retention_duration)
        p_limit = getLastDayOfPeriod(p_limit.month, p_limit.year)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        arv_started = ArvStartedDuringPeriod(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        ).filter_patients_dataframe(
            p_limit,
            start_date=p_start,
            include_null_dates=include_null_dates
        )[0]
        intersection = active_list.index.intersection(arv_started.index)
        return active_list.loc[intersection], None


class ArvRetention6MonthsPatients(ArvRetentionPatients):

    def __init__(self, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        super(ArvRetention6MonthsPatients, self).__init__(
            6,
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_6_MONTHS"


class ArvRetention12MonthsPatients(ArvRetentionPatients):

    def __init__(self, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        super(ArvRetention12MonthsPatients, self).__init__(
            12,
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_12_MONTHS"


class ArvRetention24MonthsPatients(ArvRetentionPatients):

    def __init__(self, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        super(ArvRetention24MonthsPatients, self).__init__(
            24,
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_24_MONTHS"


class ArvRetention60MonthsPatients(ArvRetentionPatients):

    def __init__(self, patients_dataframe,
                 visits_dataframe, patient_drugs_dataframe,
                 visit_drugs_dataframe):
        super(ArvRetention60MonthsPatients, self).__init__(
            60,
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_60_MONTHS"
