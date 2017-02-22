# coding: utf-8

from indicators.base_indicator import BaseIndicator


class IncludedPatients(BaseIndicator):
    """
    Basic indicator, computes the number of patients that had been included
    in the follow up, whether there are under arv, died, lost...
    """

    def get_value(self, limit_date, gender=None, age_min=None, age_max=None,
                  include_null_dates=False, **kwargs):
        df = self.filter_patients_by_category(
            limit_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            include_null_dates=include_null_dates
        )
        return len(df)
