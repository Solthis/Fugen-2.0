# coding: utf-8

from data.query import *


class FuchiaDatabase:

    def __init__(self, cursor):
        self.cursor = cursor
        self.patients_dataframe = query_patients_dataframe(self.cursor)
        self.visits_dataframe = query_visits_dataframe(self.cursor)
        self.patient_drugs_dataframe = query_patient_drugs_dataframe(self.cursor)
        self.visit_drugs_dataframe = query_visit_drugs_dataframe(self.cursor)
        self.visit_tb_dataframe = query_visit_tb_dataframe(self.cursor)
        self.references_dataframe = query_references_dataframe(self.cursor)
