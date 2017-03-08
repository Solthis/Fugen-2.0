# coding: utf-8

from reports.medical.query_bis import *


class FuchiaDatabase:

    def __init__(self, cursor):
        self.cursor = cursor
        self.patients_dataframe = query_patients_dataframe(self.cursor)
        self.visits_dataframe = query_visits_dataframe(self.cursor)
        self.patient_drugs_dataframe = query_patient_drugs_dataframe(self.cursor)
        self.visit_drugs_dataframe = query_visit_drugs_dataframe(self.cursor)
