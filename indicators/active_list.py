# coding: utf-8

from dateutil.relativedelta import relativedelta

from indicators.patient_indicator import PatientIndicator
from indicators.arv_started_patients import ArvStartedPatients
from indicators.dead_patients import DeadPatients
from indicators.transferred_patients import TransferredPatients
from indicators.lost_patients import LostPatients
from indicators.lost_back_patients import LostBackPatients


class ActiveList(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "ACTIVE_LIST"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        arv_started = ArvStartedPatients(
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
        lost_back = LostBackPatients(
            self.patients_dataframe,
            self.visits_dataframe,
            self.patient_drugs_dataframe,
            self.visit_drugs_dataframe
        )
        al = (arv_started & ~dead & ~transferred & ~lost)
        al_patients = al.filter_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        )
        return al_patients


class PreviousActiveList(ActiveList):

    @classmethod
    def get_key(cls):
        return "PREVIOUS_ACTIVE_LIST"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        return super(PreviousActiveList, self).filter_patients_dataframe(
            limit_date - relativedelta(months=1),
            start_date=start_date - relativedelta(months=1),
            include_null_dates=include_null_dates
        )
