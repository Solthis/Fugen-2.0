# coding: utf-8


from data.indicators.dead_patients import DeadPatients
from data.indicators.included_patients import IncludedPatients
from data.indicators.lost_patients import LostPatients
from data.indicators.patient_indicator import PatientIndicator

from data.indicators.transferred_patients import TransferredPatients


class FollowedPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "FOLLOWED"

    @classmethod
    def get_display_label(cls):
        return "Patients suivis"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        included = IncludedPatients(self.fuchia_database)
        dead = DeadPatients(self.fuchia_database)
        transferred = TransferredPatients(self.fuchia_database)
        lost = LostPatients(self.fuchia_database)
        followed = (included & ~dead & ~transferred & ~lost)
        return followed.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
