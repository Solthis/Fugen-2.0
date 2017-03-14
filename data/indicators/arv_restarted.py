# coding: utf-8

from dateutil.relativedelta import relativedelta
from data.indicators.arv_stopped import ArvStopped
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.active_list import ActiveList
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ArvRestartedDuringPeriod(PatientIndicator):
    """
    Patients who stopped the treatment during the previous period, and
    started it again.
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ARV_RESTARTED"

    @classmethod
    def get_display_label(cls):
        return "Traitement repris"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        stopped_prev = ArvStopped(self.fuchia_database)
        n_limit = limit_date - relativedelta(months=1)
        n_start = start_date - relativedelta(months=1)
        stopped_prev_patients = stopped_prev.get_filtered_patients_dataframe(
            getLastDayOfPeriod(n_limit.month, n_limit.year),
            start_date=getFirstDayOfPeriod(n_start.month, n_start.year),
            include_null_dates=include_null_dates
        )
        al = ActiveList(self.fuchia_database)
        active_list = al.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        idx = stopped_prev_patients.index.intersection(active_list.index)
        return active_list.loc[idx], None
