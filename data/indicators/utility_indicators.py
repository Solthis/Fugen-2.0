# coding: utf-8

from data.indicators.base_indicator import BaseIndicator
import constants


class UtilityIndicator(BaseIndicator):
    """
    Indicator displaying general information such as period, or site name.
    """

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False):
        raise NotImplementedError()


class PeriodIndicator(UtilityIndicator):

    @classmethod
    def get_key(cls):
        return "PERIOD"

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False):
        month = str(limit_date.month)
        year = str(limit_date.year)
        month = month.zfill(2)
        return "{}/{}".format(month, year)


class SiteNameIndicator(UtilityIndicator):

    @classmethod
    def get_key(cls):
        return "SITE_NAME"

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False):
        return constants.DEFAULT_SITENAME


class RegionNameIndicator(UtilityIndicator):

    @classmethod
    def get_key(cls):
        return "REGION_NAME"

    def get_value(self, limit_date, start_date=None, gender=None, age_min=None,
                  age_max=None, age_is_null=False, include_null_dates=False):
        return constants.DEFAULT_REGION_NAME
