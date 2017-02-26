# coding: utf-8

from indicators.patient_indicator import PatientIndicator


class IncludedPatients(PatientIndicator):
    """
    Basic indicator, computes the number of patients that had been included
    in the follow up, whether there are under arv, died, lost...
    """

    def get_filtered_patients_dataframe(self, limit_date, start_date=None,
                                        gender=None, age_min=None,
                                        age_max=None, age_is_null=False,
                                        include_null_dates=False):
        return self.filter_patients_by_category(
            limit_date,
            start_date=None,
            gender=gender,
            age_min=age_min,
            age_max=age_max,
            age_is_null=age_is_null,
            include_null_dates=include_null_dates
        )
