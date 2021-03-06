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


from dateutil.relativedelta import relativedelta
from data.indicators.arv_started_patients import ArvStartedDuringPeriod
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.active_list import ActiveList
from utils import getFirstDayOfPeriod, getLastDayOfPeriod


class ArvRetentionPatients(PatientIndicator):

    def __init__(self, retention_duration, fuchia_database):
        super(ArvRetentionPatients, self).__init__(
            fuchia_database
        )
        self.retention_duration = retention_duration

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        raise NotImplementedError()

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        active_list = ActiveList(
            self.fuchia_database
        ).get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        p_limit = limit_date - relativedelta(months=self.retention_duration)
        p_start = start_date - relativedelta(months=self.retention_duration)
        p_limit = getLastDayOfPeriod(p_limit.month, p_limit.year)
        p_start = getFirstDayOfPeriod(p_start.month, p_start.year)
        arv_started = ArvStartedDuringPeriod(
            self.fuchia_database
        ).get_filtered_patients_dataframe(
            p_limit,
            start_date=p_start,
            include_null_dates=include_null_dates
        )
        intersection = active_list.index.intersection(arv_started.index)
        return active_list.loc[intersection], None


class ArvRetention6MonthsPatients(ArvRetentionPatients):

    def __init__(self, fuchia_database):
        super(ArvRetention6MonthsPatients, self).__init__(
            6,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_6_MONTHS"

    @classmethod
    def get_display_label(cls):
        return "En rétention depuis 6 mois"


class ArvRetention12MonthsPatients(ArvRetentionPatients):

    def __init__(self, fuchia_database):
        super(ArvRetention12MonthsPatients, self).__init__(
            12,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_12_MONTHS"

    @classmethod
    def get_display_label(cls):
        return "En rétention depuis 12 mois"


class ArvRetention24MonthsPatients(ArvRetentionPatients):

    def __init__(self, fuchia_database):
        super(ArvRetention24MonthsPatients, self).__init__(
            24,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_24_MONTHS"

    @classmethod
    def get_display_label(cls):
        return "En rétention depuis 24 mois"


class ArvRetention60MonthsPatients(ArvRetentionPatients):

    def __init__(self, fuchia_database):
        super(ArvRetention60MonthsPatients, self).__init__(
            60,
            fuchia_database
        )

    @classmethod
    def get_key(cls):
        return "ARV_RETENTION_60_MONTHS"

    @classmethod
    def get_display_label(cls):
        return "En rétention depuis 60 mois"
