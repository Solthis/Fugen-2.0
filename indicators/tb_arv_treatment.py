# coding: utf-8

from indicators.patient_indicator import PatientIndicator
from indicators.active_list import ActiveList
from indicators.tb_treatment import UnderTbTreatmentPatients


class UnderTbTreatmentAndArvPatients(PatientIndicator):

    def under_arv(self):
        return False

    @classmethod
    def get_key(cls):
        return "TB_ARV_TREATMENT"

    def filter_patients_dataframe(self, limit_date, start_date=None,
                                  include_null_dates=False):
        tb_treatment = UnderTbTreatmentPatients(self.fuchia_database)
        active_list = ActiveList(self.fuchia_database)
        arv_and_tb_treatment = (tb_treatment & active_list)
        return arv_and_tb_treatment.get_filtered_patients_dataframe(
            limit_date,
            start_date=start_date,
            include_null_dates=include_null_dates
        ), None
