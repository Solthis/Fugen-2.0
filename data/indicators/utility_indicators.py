# coding: utf-8

# Copyright 2017 Solthis.
#
# This file is part of Fugen 2.0.
#
# Fugen 2.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fugen 2.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fugen 2.0. If not, see <http://www.gnu.org/licenses/>.


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
