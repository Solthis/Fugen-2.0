# coding: utf-8

import pandas as pd

from data.indicators.base_indicator import BaseIndicator


class PatientIndicator(BaseIndicator):
    """
    Indicator on patients. The indicator is a number of patients that match
    some criterion defined by the indicator.
    Patients indicators can be combined to create intersection indicators.
    """

    def __init__(self, fuchia_database):
        super(PatientIndicator, self).__init__(fuchia_database)
        self._cached_patients_df = None
        self._cached_event_dates = None
        self.last_limit_date = None
        self.last_start_date = None
        self.last_include_null = None

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def under_arv(self):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        raise NotImplementedError()

    def get_filtered_patients_dataframe(self, limit_date, start_date=None,
                                        include_null_dates=False):
        b1 = self.last_limit_date == limit_date
        b2 = self.last_start_date == start_date
        b3 = self.last_include_null == include_null_dates
        b = b1 & b2 & b3
        if not b:
            r = self.filter_patients_dataframe(
                limit_date,
                start_date=start_date,
                include_null_dates=include_null_dates
            )
            self._cached_patients_df = r[0]
            self._cached_event_dates = r[1]
            self.last_limit_date = limit_date
            self.last_start_date = start_date
            self.last_include_null = include_null_dates
        return self._cached_patients_df

    def get_event_dates(self, limit_date, start_date=None,
                        include_null_dates=False):
        b1 = self.last_limit_date == limit_date
        b2 = self.last_start_date == start_date
        b3 = self.last_include_null == include_null_dates
        b = b1 & b2 & b3
        if not b:
            r = self.filter_patients_dataframe(
                limit_date,
                start_date=start_date,
                include_null_dates=include_null_dates
            )
            self._cached_patients_df = r[0]
            self._cached_event_dates = r[1]
            self.last_limit_date = limit_date
            self.last_start_date = start_date
            self.last_include_null = include_null_dates
        return self._cached_event_dates

    def get_filtered_by_category(self, limit_date, start_date=None,
                                 gender=None, age_min=None, age_max=None,
                                 include_null_dates=False, age_is_null=False,
                                 post_filter_index=None):
        patients = self.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        if post_filter_index is not None:
            intersection = patients.index.intersection(post_filter_index)
            patients = patients.loc[intersection]
        category_filter = pd.notnull(patients['id'])
        if gender is not None:
            category_filter &= (patients['gender'] == gender)
        if age_is_null:
            c = category_filter & pd.isnull(patients['age_at_date'])
            return patients[c]
        if age_min is not None:
            category_filter &= (patients['age_at_date'] >= age_min)
        if age_max is not None:
            category_filter &= (patients['age_at_date'] < age_max)
        return patients[category_filter]

    def get_value(self, limit_date, start_date=None, gender=None,
                  age_min=None, age_max=None, age_is_null=False,
                  include_null_dates=False, post_filter_index=None):
        patients = self.get_filtered_by_category(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        return len(patients)

    def __or__(self, other):
        return UnionPatientIndicator(self, other)

    def __and__(self, other):
        return IntersectionPatientIndicator(self, other)

    def __invert__(self):
        return InvertedIndicator(self)


class AdditionPatientIndicator(PatientIndicator):
    pass


class SubstractionPatientIndicator(PatientIndicator):
    pass


class MultiplicationPatientIndicator(PatientIndicator):
    pass


class DivisionPatientIndicator(PatientIndicator):
    pass


class UnionPatientIndicator(PatientIndicator):
    """
    Result of the union of two patient indicators, using the | (pipe)
    operator.
    """

    def __init__(self, indicator_a, indicator_b):
        self.indicator_a = indicator_a
        self.indicator_b = indicator_b
        self._cached_patients_df = None
        self.last_limit_date = None
        self.last_start_date = None
        self.last_include_null = None

    @property
    def patients_dataframe(self):
        return self.indicator_a.patients_dataframe

    @property
    def visits_dataframe(self):
        return self.indicator_a.visits_dataframe

    @property
    def patient_drugs_dataframe(self):
        return self.indicator_a.patient_drugs_dataframe

    @property
    def visit_drugs_dataframe(self):
        return self.indicator_a.visit_drugs_dataframe

    def under_arv(self):
        a = self.indicator_a.under_arv()
        b = self.indicator_b.under_arv()
        return a and b

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df_a = self.indicator_a.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        df_b = self.indicator_b.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        df_c = pd.merge(
            df_a, df_b,
            left_index=True, right_index=True,
            suffixes=('', '_y'),
            how='outer'
        )
        return df_c[df_a.columns], None


class IntersectionPatientIndicator(PatientIndicator):
    """
    Result of the intersection of two patient indicators, using the &
    operator.
    """

    def __init__(self, indicator_a, indicator_b):
        self.indicator_a = indicator_a
        self.indicator_b = indicator_b
        self._cached_patients_df = None
        self.last_limit_date = None
        self.last_start_date = None
        self.last_include_null = None

    @property
    def patients_dataframe(self):
        return self.indicator_a.patients_dataframe

    @property
    def visits_dataframe(self):
        return self.indicator_a.visits_dataframe

    @property
    def patient_drugs_dataframe(self):
        return self.indicator_a.patient_drugs_dataframe

    @property
    def visit_drugs_dataframe(self):
        return self.indicator_a.visit_drugs_dataframe

    def under_arv(self):
        a = self.indicator_a.under_arv()
        b = self.indicator_b.under_arv()
        return a or b

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df_a = self.indicator_a.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        df_b = self.indicator_b.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        df_c = pd.merge(
            df_a, df_b,
            left_index=True, right_index=True,
            suffixes=('', '_y'),
            how='inner'
        )
        return df_c[df_a.columns], None


class DuringPeriodIndicator(PatientIndicator):

    def __init__(self, indicator, fuchia_database):
        super(DuringPeriodIndicator, self).__init__(fuchia_database)
        self.indicator = indicator

    def under_arv(self):
        return self.indicator.under_arv()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df = self.indicator.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        event_dates = self.indicator.get_event_dates(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        if event_dates is None:
            raise NotImplementedError(
                "{} is not compatible with DuringPeriodIndicator.".format(
                    self.indicator.get_key()
                )
            )
        c = (event_dates >= start_date) & (event_dates <= limit_date)
        during_period = event_dates[c]
        if len(during_period) == 0:
            return df[:0], during_period
        return df.loc[during_period.index], during_period

    @classmethod
    def get_key(cls):
        raise NotImplementedError()


class InvertedIndicator(PatientIndicator):

    def __init__(self, indicator):
        self.indicator = indicator
        self._cached_patients_df = None
        self.last_limit_date = None
        self.last_start_date = None
        self.last_include_null = None

    @property
    def patients_dataframe(self):
        return self.indicator.patients_dataframe

    @property
    def visits_dataframe(self):
        return self.indicator.visits_dataframe

    @property
    def patient_drugs_dataframe(self):
        return self.indicator.patient_drugs_dataframe

    @property
    def visit_drugs_dataframe(self):
        return self.indicator.visit_drugs_dataframe

    def under_arv(self):
        return self.indicator.under_arv()

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df = self.indicator.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        patients = self.indicator.patients_dataframe
        diff = patients.index.difference(df.index)
        return patients.loc[diff], None
