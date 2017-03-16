# coding: utf-8

import pandas as pd

import constants
from data.indicators.active_list import ActiveList


class ArvRepartition:
    """
    Compute the repartition of ARV treatments.
    """

    def __init__(self, fuchia_database):
        self.fuchia_database = fuchia_database

    def get_active_list_repartition(self, limit_date, start_date,
                                    include_null_dates=None):
        active_list = ActiveList(
            self.fuchia_database
        )
        patients = active_list.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visits = active_list.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = visits[pd.notnull(visits['arv_received'])]
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        last_visits = last_visits.loc[patients.index]
        # Patient drugs
        diff = patients.index.difference(
            visits.loc[last_visits]['patient_id']
        )
        patients = patients.loc[diff]['arv_drugs']
        patients = patients.value_counts()
        drugs = visits.loc[last_visits].groupby('arv_received')['patient_id'].count()
        drugs.loc[patients.index] = drugs + patients
        return drugs.sort_values(ascending=False)

    def get_prescriptions_repartition(self, limit_date, start_date,
                                      include_null_dates=None):
        active_list = ActiveList(
            self.fuchia_database
        )
        visits = active_list.filter_visits_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        drugs = visits.loc[last_visits].groupby('arv_received')['patient_id'].count()
        return drugs.sort_values(ascending=False)


