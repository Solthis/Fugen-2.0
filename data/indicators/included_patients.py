# coding: utf-8

from data.indicators.patient_indicator import PatientIndicator


class IncludedPatients(PatientIndicator):
    """
    Basic indicator, computes the number of patients that had been included
    in the follow up, whether there are under arv, died, lost...
    """

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "INCLUDED"

    @classmethod
    def get_display_label(cls):
        return "Patients inscrits dans la base"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        return self.filter_patients_by_category(
            limit_date,
            start_date=None,
            include_null_dates=include_null_dates
        ), None
