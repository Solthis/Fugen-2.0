# coding: utf-8

from indicators.patient_indicator import PatientIndicator
from indicators.active_list import PreviousActiveList
from indicators.arv_started_patients import ArvStartedDuringPeriod
from indicators.incoming_transfer_patients import ArvIncomingTransferPatientsDuringPeriod
from indicators.lost_back_patients import ArvLostBackPatients


class ReceivedArvDuringPeriod(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "RECEIVED_ARV_DURING_PERIOD"

    def __init__(self, fuchia_database):
        super(ReceivedArvDuringPeriod, self).__init__(fuchia_database)
        self.a = PreviousActiveList(self.fuchia_database)
        self.b = ArvStartedDuringPeriod(self.fuchia_database)
        self.c = ArvIncomingTransferPatientsDuringPeriod(self.fuchia_database)
        self.d = ArvLostBackPatients(self.fuchia_database)

    def get_value(self, limit_date, start_date=None, gender=None,
                  age_min=None, age_max=None, age_is_null=False,
                  include_null_dates=False, post_filter_index=None):
        a = self.a.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        b = self.b.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        c = self.c.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        d = self.d.get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
        return a + b + c + d
