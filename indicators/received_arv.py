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

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        a = self.a.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0].index
        b = self.b.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0].index
        c = self.c.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0].index
        d = self.d.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )[0].index
        idx = a.union(b).union(c).union(d)
        return patients.loc[idx], None

    def get_value(self, limit_date, start_date=None, gender=None,
                  age_min=None, age_max=None, age_is_null=False,
                  include_null_dates=False, post_filter_index=None):
        return (self.a + self.b + self.c + self.d).get_value(
            limit_date,
            start_date=start_date,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates,
            post_filter_index=post_filter_index
        )
