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
        included = IncludedPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        dead = DeadPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        transferred = TransferredPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        lost = LostPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        followed = (included & ~dead & ~transferred & ~lost)
        return followed.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
