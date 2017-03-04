# coding: utf-8

from indicators.patient_indicator import PatientIndicator


class IncludedPatients(PatientIndicator):
    """
    Basic indicator, computes the number of patients that had been included
    in the follow up, whether there are under arv, died, lost...
    """

    @classmethod
    def get_key(cls):
        return "INCLUDED"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        return self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        ), None
