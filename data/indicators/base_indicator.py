# coding: utf-8

import pandas as pd

from data.fuchia_database import FuchiaDatabase
import constants


INDICATORS_REGISTRY = {}


class IndicatorMeta(type):

    FUCHIA_DB_INSTANCE = None
    INSTANCES = {}

    def __call__(cls, *args, **kwargs):
        if len(args) >= 0 and isinstance(args[0], FuchiaDatabase):
            db = args[0]
            if db != cls.FUCHIA_DB_INSTANCE:
                # Invalidate cache
                cls.INSTANCES = {}
                cls.FUCHIA_DB_INSTANCE = db
            if cls not in cls.INSTANCES:
                cls.INSTANCES[cls] = super(
                    IndicatorMeta,
                    cls
                ).__call__(*args, **kwargs)
            return cls.INSTANCES[cls]
        return super(IndicatorMeta, cls).__call__(*args, **kwargs)

    def __init__(cls, *args, **kwargs):
        try:
            INDICATORS_REGISTRY[cls.get_key()] = {
                'class': cls,
            }
        except NotImplementedError:
            pass
        return super(IndicatorMeta, cls).__init__(cls)


class BaseIndicator(metaclass=IndicatorMeta):
    """
    Abstract base class for an indicator.
    """

    def __init__(self, fuchia_database):
        self.fuchia_database = fuchia_database

    @property
    def patients_dataframe(self):
        return self.fuchia_database.patients_dataframe

    @property
    def visits_dataframe(self):
        return self.fuchia_database.visits_dataframe

    @property
    def patient_drugs_dataframe(self):
        return self.fuchia_database.patient_drugs_dataframe

    @property
    def visit_drugs_dataframe(self):
        return self.fuchia_database.visit_drugs_dataframe

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_at_date(self, limit_date, start_date=None,
                                include_null_dates=False):
        """
        Filter the patients dataframe to only retain those who entered the
        follow up before the limit date. For each patient, also compute the
        age at the given limit age and add it in a new column called
        'age_at_date'.
        :param limit_date: The limit date (included) to filter on.
        :param start_date: If given, only return the patients who had a visit
        between the start_date and the limit date (both included).
        :param include_null_dates: If True, will include the patients with a null
        date.
        :return: The filtered dataframe.
        """
        if pd.isnull(limit_date):
            return self.patients_dataframe
        visits_filtered = self.filter_visits_at_date(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        c = self.patients_dataframe['id'].isin(visits_filtered['patient_id'])
        df = self.patients_dataframe[c]
        age_at_date_col = df.apply(
            lambda i: get_age_at_date(i, limit_date),
            axis=1
        )
        if len(df) == 0:
            return df
        return df.assign(age_at_date=age_at_date_col)

    def filter_visits_at_date(self, limit_date, start_date=None,
                              include_null_dates=False):
        """
        Filter the visits dataframe to only retain events that happened before
        the limit date.
        :param limit_date: The limit date (included) to filter on.
        :param start_date: If given, only return the visits between the
        start_date and the limit date (both included).
        :param include_null_dates: If True, will include the event with a null date.
        :return: The filtered dataframe.
        """
        if pd.isnull(limit_date):
            return self.visits_dataframe
        date_filter = (self.visits_dataframe['visit_date'] <= limit_date)
        if start_date:
            date_filter &= (self.visits_dataframe['visit_date'] >= start_date)
        if include_null_dates:
            null_filter = pd.isnull(self.visits_dataframe['visit_date'])
            return self.visits_dataframe[date_filter | null_filter]
        return self.visits_dataframe[date_filter]

    def filter_patients_by_category(self, limit_date, start_date=None,
                                    gender=None, age_min=None,
                                    age_max=None, age_is_null=False,
                                    include_null_dates=False):
        """
        Filter the patients dataframe with a limit date and a category.
        A category is a combination of a gender (male, female or both)
        constraint and one or two age constraints (min, max, min and max).
        Note that the min age constraint is greater or equal (>=)
        and the max age constraint is strictly lesser (<).
        :param limit_date: The limit date to filter on.
        :param start_date: If given, only return the patients who had a visit
        between the start_date and the limit date (both included).
        :param gender: The gender to filter on. None means both.
        None by default.
        :param age_min: The minimum age to filter on. None means no minimum.
        None by default.
        :param age_max: The maximum age to filter on. None means no maximum.
        None by default.
        :param age_is_null: If true, only return patients with a null value
        for the age.
        :param include_null_dates: If true, include patients with a null
        inclusion date. False by default.
        :return: The filtered dataframe.
        """
        df = self.filter_patients_at_date(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        # Fake filter - Always true
        category_filter = pd.notnull(df['id'])
        if gender is not None:
            category_filter &= (df['gender'] == gender)
        if age_is_null:
            return df[category_filter & pd.isnull(df['age_at_date'])]
        if age_min is not None:
            category_filter &= (df['age_at_date'] >= age_min)
        if age_max is not None:
            category_filter &= (df['age_at_date'] < age_max)
        return df[category_filter]

    def filter_visits_by_category(self, limit_date, start_date=None,
                                  gender=None, age_min=None,
                                  age_max=None, age_is_null=False,
                                  include_null_dates=False):
        """
        Filter the visits dataframe with a limit date and a category.
        A category is a combination of a gender (male, female or both)
        constraint and one or two age constraints (min, max, min and max).
        Note that the min age constraint is greater or equal (>=)
        and the max age constraint is strictly lesser (<).
        :param limit_date: The limit date to filter on.
        :param start_date: If given, only return the visits between the
        start_date and the limit date (both included).
        :param gender: The gender to filter on. None means both.
        :param age_min: The minimum age to filter on. None means no minimum.
        None by default.
        :param age_max: The maximum age to filter on. None means no maximum.
        None by default.
        :param age_is_null: If true, only return patients with a null value
        for the age.
        :param include_null_dates: If true, include data with a null date.
        False by default.
        :return: The filtered dataframe.
        """
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null
        )
        visits = self.filter_visits_at_date(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        df = visits[visits['patient_id'].isin(patients.index)]
        return df

    def filter_patient_drugs_by_category(self, limit_date, start_date=None,
                                         gender=None, age_min=None,
                                         age_max=None, age_is_null=False,
                                         include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null
        )
        df = self.patient_drugs_dataframe
        df = df[df['beginning'] <= limit_date]
        return df[df['patient_id'].isin(patients['id'])]

    def filter_visit_drugs_by_category(self, limit_date, start_date=None,
                                       gender=None, age_min=None,
                                       age_max=None, age_is_null=False,
                                       include_null_dates=False):
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null
        )
        df = self.visit_drugs_dataframe
        return df[df['visit_id'].isin(visits['id'])]

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False):
        return NotImplementedError()

    def __add__(self, other):
        return AdditionIndicator(self, other)

    def __sub__(self, other):
        return SubtractionIndicator(self, other)


class AdditionIndicator(BaseIndicator):

    def __init__(self, indicator_a, indicator_b):
        super(AdditionIndicator, self).__init__(indicator_a.fuchia_database)
        self.indicator_a = indicator_a
        self.indicator_b = indicator_b

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False,
                  post_filter_index=None):
        a = self.indicator_a.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        b = self.indicator_b.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        return a + b


class SubtractionIndicator(BaseIndicator):

    def __init__(self, indicator_a, indicator_b):
        super(SubtractionIndicator, self).__init__(indicator_a.fuchia_database)
        self.indicator_a = indicator_a
        self.indicator_b = indicator_b

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False,
                  post_filter_index=None):
        a = self.indicator_a.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        b = self.indicator_b.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        return a - b


def get_age_at_date(patient_record, limit_date):
    birth_date = patient_record['birth_date']
    age_in_days = None
    if not pd.isnull(birth_date):
        age_in_days = (limit_date.date() - birth_date.date()).days
    else:
        age = patient_record['age']
        age_unit = patient_record['age_unit']
        age_date = patient_record['age_date']
        if pd.isnull(age_date) or pd.isnull(age):
            return None
        delta_in_days = 0
        if pd.notnull(age_date):
            delta_in_days = (limit_date.date() - age_date.date()).days
        if age is not None and age_date is not None and age_unit is not None:
            if age_unit == constants.MONTH_UNIT:
                age_in_days = age * 30
            elif age_unit == constants.YEAR_UNIT:
                age_in_days = age * 365
            elif age_unit == constants.DAY_UNIT:
                age_in_days = age
        age_in_days += delta_in_days
    return age_in_days // 365
