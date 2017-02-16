# -*- coding: utf-8 -*

"""
Module containing the medical indicators descriptions.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

#================================#
# MedicalAtomic Indicators types #
#================================#

E1 = 'E1'  # Number of new patients put under ARV treatment.
E2 = 'E2'  # Number of patient back in the treatment.
E3 = 'E3'  # Number of dead patients.
E4 = 'E4'  # Number of transfered patients.
E5 = 'E5'  # Number of lost from view patients
E6 = 'E6'  # Number of tuberculous patients put under ARV treatment.

E7 = 'E7'  # Number of ARV incoming transfer patients.

A1 = 'A1'  # Number of HIV+ patients who where diagnosed tuberculous.
A2 = 'A2'  # Number of patients who had a CD4 count.
A3 = 'A3'  # Number of patients who a had viral load.
A4 = 'A4'  # Number of patients receiving Cotrimoxazole.

S1 = 'S1'  # Number of patients followed under ARV since 12 months.
S2 = 'S2'  # Number of patients followed under ARV since 24 months.
S3 = 'S3'  # Number of patients followed under ARV since 36 months.
S4 = 'S4'  # Number of patients followed under ARV since 48 months.

B1 = 'B1'  # Number of patients followed under ARV.
B2 = 'B2'  # Total number of patients followed.

E = [E1, E2, E3, E4, E5, E6, E7]
A = [A1, A2, A3, A4]
S = [S1, S2, S3, S4]
B = [B1, B2]

INDICATOR_TYPE_KEYS = E + A + S + B


#=====================================#
# MedicalAtomic indicators categories #
#=====================================#


MA = 'MA'  # Male adult.
FA = 'FA'  # Female adult.
MC = 'MC'  # Male child.
FC = 'FC'  # Female child.

INDICATOR_CATEGORY_KEYS = [MA, FA, MC, FC]

#==========================================#
# Description of indicators and categories #
#==========================================#

CATEGORIES_DESC = { MA: "Adultes masculins",
                    FA: "Adultes féminins",
                    MC: "Enfants masculins",
                    FC: "Enfants féminins", }

INDICATORS_DESC = { E1: "Nouveaux patients sous ARV",
                    E2: "Patients de retour dans le traitement",
                    E3: "Patients sous ARV décédes",
                    E4: "Patients sous ARV transférés",
                    E5: "Patients sous ARV perdus de vue",
                    E6: "Patients tuberculeux mis sous ARV",
                    E7: "Patients sous ARV transférés entrants",
                    A1: "Patients VIH+ ayant développé une tuberculose",
                    A2: "Patients ayant eu un comptage CD4",
                    A3: "Patients ayant eu une charge virale",
                    A4: "Patients recevant du cotrimoxazole",
                    S1: "Patients suivis sous ARV depuis 12 mois",
                    S2: "Patients suivis sous ARV depuis 24 mois",
                    S3: "Patients suivis sous ARV depuis 36 mois",
                    S4: "Patients suivis sous ARV depuis 48 mois",
                    B1: "Patients suivis sous ARV",
                    B2: "Patients suivis", }
