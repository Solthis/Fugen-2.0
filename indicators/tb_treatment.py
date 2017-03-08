# coding: utf-8

import pandas as pd

from indicators.patient_indicator import PatientIndicator
from indicators.active_list import ActiveList


class TbTreatmentStartedDuringPeriod(PatientIndicator):
    """
    Patients who started a tb treatment during a given period.
    """

    @classmethod
    def get_key(cls):
        return "TB_TREATMENT_STARTED_DURING_PERIOD"

    def under_arv(self):
        return False

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        active_list = ActiveList(
            self.fuchia_database
        ).filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        visits_tb = self.fuchia_database.visit_tb_dataframe
        c1 = visits_tb['treatment_start'] >= start_date
        c2 = visits_tb['treatment_start'] <= limit_date
        visits_tb = visits_tb[c1 & c2]
        ids = pd.Index(visits_tb['patient_id'].unique())
        tb_index = active_list.index.intersection(ids)
        return active_list.loc[tb_index], None
