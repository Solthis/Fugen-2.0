# coding: utf-8

import pandas as pd

from indicators.active_list import ActiveList
import constants


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
        visit_drugs = active_list.filter_visit_drugs_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        patient_drugs = active_list.filter_patient_drugs_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        c = visit_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        visit_drugs = visit_drugs[~c]
        visit_drugs = visit_drugs.sort_values(['visit_id', 'drug_id'])
        visit_drugs = visit_drugs.groupby('visit_id')['drug_id'].apply(tuple)
        visits = visits.assign(drugs=visit_drugs)
        visits = visits[pd.notnull(visits['drugs'])]
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        last_visits = last_visits.loc[patients.index]
        # Patient drugs
        c2 = patient_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        patient_drugs = patient_drugs[~c2]
        patient_drugs = patient_drugs.sort_values(['patient_id', 'drug_id'])
        patient_drugs = patient_drugs.groupby('patient_id')['drug_id']\
            .apply(tuple)
        diff = patient_drugs.index.difference(
            visits.loc[last_visits]['patient_id']
        )
        patient_drugs = patient_drugs.loc[diff]
        patient_drugs = patient_drugs.value_counts()
        drugs = visits.loc[last_visits].groupby('drugs')['patient_id'].count()
        drugs.loc[patient_drugs.index] = drugs + patient_drugs
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
        visit_drugs = active_list.filter_visit_drugs_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        visit_drugs = visit_drugs.sort_values(['visit_id', 'drug_id'])
        c = visit_drugs['drug_id'].isin(constants.EXCLUDED_DRUGS)
        visit_drugs = visit_drugs[~c]
        visit_drugs = visit_drugs.groupby('visit_id')['drug_id'].apply(tuple)
        visits = visits.assign(drugs=visit_drugs)
        last_visits = visits.groupby('patient_id')['visit_date'].idxmax()
        drugs = visits.loc[last_visits].groupby('drugs')['patient_id'].count()
        return drugs.sort_values(ascending=False)


