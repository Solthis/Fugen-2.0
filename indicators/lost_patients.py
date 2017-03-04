# coding: utf-8

from indicators.patient_indicator import PatientIndicator


class IncomingTransferPatientsDuringPeriod(PatientIndicator):
    """
    Indicator that compute the number of patients already under ARV who were
    transferred from another center during the given period
    (between start_date and limit_date).
    """

    @classmethod
    def get_key(cls):
        return "INCOMING_TRANSFER_DURING_PERIOD"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        patients = self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        visits = self.filter_visits_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        )
        return None, None
