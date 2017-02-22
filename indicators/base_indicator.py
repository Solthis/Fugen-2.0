# coding: utf-8

import pandas as pd

import constants


class BaseIndicator:
    """
    Abstract base class for an indicator.
    """

    def __init__(self, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        self.patients_dataframe = patients_dataframe
        self.visits_dataframe = visits_dataframe
        self.patient_drugs_dataframe = patient_drugs_dataframe
        self.visit_drugs_dataframe = visit_drugs_dataframe

    def filter_patients_at_date(self, limit_date, include_null=False):
        """
        Filter the patients dataframe to only retain those who entered the
        follow up before the limit date. For each patient, also compute the
        age at the given limit age and add it in a new column called
        'age_at_date'.
        :param limit_date: The limit date (included) to filter on.
        :param include_null: If True, will include the patients with a null
        date.
        :return: The filtered dataframe.
        """
        if pd.isnull(limit_date):
            return self.patients_dataframe
        visits_filtered = self.filter_visits_at_date(limit_date, include_null)
        c = self.patients_dataframe['id'].isin(visits_filtered['patient_id'])
        df = self.patients_dataframe[c]
        age_at_date_col = df.apply(
            lambda i: get_age_at_date(i, limit_date),
            axis=1
        )
        return df.assign(age_at_date=age_at_date_col)

    def filter_visits_at_date(self, limit_date, include_null=False):
        """
        Filter the visits dataframe to only retain events that happened before
        the limit date.
        :param limit_date: The limit date (included) to filter on.
        :param include_null: If True, will include the event with a null date.
        :return: The filtered dataframe.
        """
        if pd.isnull(limit_date):
            return self.visits_dataframe
        date_filter = (self.visits_dataframe['visit_date'] <= limit_date)
        if include_null:
            null_filter = pd.isnull(self.visits_dataframe['visit_date'])
            return self.visits_dataframe[date_filter | null_filter]
        return self.visits_dataframe[date_filter]

    def filter_patients_by_category(self, limit_date, gender=None,
                                    age_min=None, age_max=None,
                                    include_null_dates=False):
        """
        Filter the patients dataframe with a limit date and a category.
        A category is a combination of a gender (male, female or both)
        constraint and one or two age constraints (min, max, min and max).
        Note that the min age constraint is greater or equal (>=)
        and the max age constraint is strictly lesser (<).
        :param limit_date: The limit date to filter on.
        :param gender: The gender to filter on. None means both.
        None by default.
        :param age_min: The minimum age to filter on. None means no minimum.
        None by default.
        :param age_max: The maximum age to filter on. None means no maximum.
        None by default.
        :param include_null_dates: If true, include patients with a null
        inclusion date. False by default.
        :return: The filtered dataframe.
        """
        df = self.filter_patients_at_date(limit_date, include_null_dates)
        # Fake filter - Always true
        category_filter = pd.notnull(df['id'])
        if gender is not None:
            category_filter &= (df['gender'] == gender)
        if age_min is not None:
            category_filter &= (df['age_at_date'] >= age_min)
        if age_max is not None:
            category_filter &= (df['age_at_date'] < age_max)
        return df[category_filter]

    def filter_visits_by_category(self, limit_date, gender=None,
                                  age_min=None, age_max=None,
                                  include_null_dates=False):
        """
        Filter the visits dataframe with a limit date and a category.
        A category is a combination of a gender (male, female or both)
        constraint and one or two age constraints (min, max, min and max).
        Note that the min age constraint is greater or equal (>=)
        and the max age constraint is strictly lesser (<).
        :param limit_date: The limit date to filter on.
        :param gender: The gender to filter on. None means both.
        :param age_min: The minimum age to filter on. None means no minimum.
        None by default.
        :param age_max: The maximum age to filter on. None means no maximum.
        None by default.
        :param include_null_dates: If true, include data with a null date.
        False by default.
        :return: The filtered dataframe.
        """
        patients = self.filter_patients_by_category(
            limit_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max
        )
        visits = self.filter_visits_at_date(limit_date, include_null_dates)
        df = visits[visits['patient_id'].isin(patients['id'])]
        return df

    def filter_patient_drugs_by_category(self, limit_date, gender=None,
                                         age_min=None, age_max=None,
                                         include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max
        )
        df = self.patient_drugs_dataframe
        df = df[df['beginning'] <= limit_date]
        return df[df['patient_id'].isin(patients['id'])]

    def filter_visit_drugs_by_category(self, limit_date, gender=None,
                                       age_min=None, age_max=None,
                                       include_null_dates=False):
        visits = self.filter_visits_by_category(
            limit_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max
        )
        df = self.visit_drugs_dataframe
        return df[df['visit_id'].isin(visits['id'])]

    def get_value(self, limit_date, gender=None, age_min=None, age_max=None,
                  include_null_dates=False, **kwargs):
        return NotImplementedError()


def get_age_at_date(patient_record, limit_date):
    birth_date = patient_record['birth_date']
    age_in_days = constants.DEFAULT_AGE * 365
    if not pd.isnull(birth_date):
        age_in_days = (limit_date - birth_date.date()).days
    else:
        age = patient_record['age']
        age_unit = patient_record['age_unit']
        age_date = patient_record['age_date']
        delta_in_days = 0
        if pd.notnull(age_date):
            delta_in_days = (limit_date - age_date.date()).days
        if age is not None and age_date is not None and age_unit is not None:
            if age_unit == constants.MONTH_UNIT:
                age_in_days = age * 30
            elif age_unit == constants.YEAR_UNIT:
                age_in_days = age * 365
            elif age_unit == constants.DAY_UNIT:
                age_in_days = age
        age_in_days += delta_in_days
    return age_in_days // 365
