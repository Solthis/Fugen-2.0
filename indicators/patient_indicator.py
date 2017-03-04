# coding: utf-8

import pandas as pd

from indicators.base_indicator import BaseIndicator


class PatientIndicator(BaseIndicator):
    """
    Indicator on patients. The indicator is a number of patients that match
    some criterion defined by the indicator.
    Patients indicators can be combined to create intersection indicators.
    """

    def __init__(self, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        super(PatientIndicator, self).__init__(
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )
        self._cached_patients_df = None
        self._cached_event_dates = None
        self.last_limit_date = None
        self.last_start_date = None
        self.last_include_null = None

    @classmethod
    def get_key(cls):
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

    def get_filtered_by_category(self, limit_date, start_date=None,
                                 gender=None, age_min=None, age_max=None,
                                 include_null_dates=False, age_is_null=False):
        patients = self.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
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
                  include_null_dates=False):
        patients = self.get_filtered_by_category(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates
        )
        return len(patients)

    def __or__(self, other):
        return UnionPatientIndicator(self, other)

    def __and__(self, other):
        return IntersectionPatientIndicator(self, other)


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

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df_a = self.indicator_a.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        df_b = self.indicator_b.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        df_c = pd.merge(
            df_a, df_b,
            left_index=True, right_index=True,
            suffixes=('', '_y'),
            how='outer'
        )[0]
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

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df_a = self.indicator_a.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        df_b = self.indicator_b.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0]
        df_c = pd.merge(
            df_a, df_b,
            left_index=True, right_index=True,
            suffixes=('', '_y'),
            how='inner'
        )[0]
        return df_c[df_a.columns], None


class DuringPeriodIndicator(PatientIndicator):

    def __init__(self, indicator, patients_dataframe, visits_dataframe,
                 patient_drugs_dataframe, visit_drugs_dataframe):
        super(PatientIndicator, self).__init__(
            patients_dataframe,
            visits_dataframe,
            patient_drugs_dataframe,
            visit_drugs_dataframe
        )
        self.indicator = indicator

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        df, event_dates = self.indicator.filter_patients_dataframe(
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
        return df.loc[during_period.index], during_period

    @classmethod
    def get_key(cls):
        raise NotImplementedError()
