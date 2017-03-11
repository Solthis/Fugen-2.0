# coding: utf-8


from indicators.patient_indicator import PatientIndicator
from indicators.included_patients import IncludedPatients
from indicators.dead_patients import DeadPatients
from indicators.transferred_patients import TransferredPatients
from indicators.lost_patients import LostPatients


class FollowedPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "FOLLOWED"

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
