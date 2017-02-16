# -*- coding: utf-8 -*

'''
Module for querying the necessary information for generating a 
medical report.

@author: Dimitri Justeau <dimitri.justeau@gmail.com>
'''

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import constants
import utils


### The driver for accessing the Microsoft Access database ###
ACCESS_DRIVER = constants.ACCESS_DRIVER

### The password of the Fuchia database ###
FUCHIADB_PASSWORD = constants.FUCHIADB_PASSWORD


#========================#
# Medical report queries #
#========================#

### Subquery that recover necessary informations from the Patient table ###
PATIENTS = \
'''
SELECT TbPatient.FdxReference AS idx,
        TbPatient.FdsId AS patient_code,
        TbPatient.FdnHIV AS hiv,
        TbPatient.FdnGender AS gender,
        TbPatient.FdnAge AS age,
        TbPatient.FdnAgeUnit AS age_unit,
        TbPatient.FddAgeDate AS age_date,
        TbPatient.FddBirth AS birth_date,
        TbPatient.FddTransfered AS transfered,
        TbPatient.FddDecentralized AS decentralized,
        TbPatient.FddDead AS dead,
        TbReference.FdnValue AS entry_mode,
        TbReference.FdsLookup as entry_mode_lookup
FROM TbPatient
LEFT JOIN TbReference
    ON TbPatient.FdxReferenceModeEntry = TbReference.FdxReference
WHERE TbPatient.FdnHIV = {hiv_positive}
'''

### Subquery that get for each patient the first patient drug recorded ###
MIN_PATIENT_DRUG = \
'''
SELECT TbPatient.FdxReference as patient_idx,
        MIN(TbPatientDrug.FddBeginning) as min_patient_drug,
        MIN(TbPatientDrug.FddCreated) as created_patient_drug
FROM (TbPatient
LEFT JOIN TbPatientDrug
    ON TbPatient.FdxReference = TbPatientDrug.FdxReferencePatient)
LEFT JOIN TbReference
    ON TbPatientDrug.FdxReferenceDrug = TbReference.FdxReference
WHERE TbReference.FdnValue NOT IN ({excluded_drugs})
    AND (TbPatientDrug.FddBeginning < #{limit_date}#
        OR TbPatientDrug.FddBeginning IS NULL)
GROUP BY TbPatient.FdxReference
'''

### Subquery that get for each patient the first visit-drug date recorded ###
MIN_VISIT_DRUG = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        MIN(TbFollowUp.FddVisit) as min_visit_drug
FROM (TbFollowUp
LEFT JOIN TbFollowUpDrug
    ON TbFollowUp.FdxReference = TbFollowUpDrug.FdxReferenceFollowUp)
LEFT JOIN TbReference
    ON TbFollowUpDrug.FdxReferenceDrug = TbReference.FdxReference
WHERE TbReference.FdnValue NOT IN({excluded_drugs})
    AND TbFollowUp.FddVisit < #{limit_date}#
GROUP BY TbFollowUp.FdxReferencePatient
'''

### Subquery that get for each patient the visit bounds ###
VISIT_BOUNDS = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        TbFollowUp.FddVisit,
        TbFollowUp.FddVisitNext as last_next_visit,
        bounds.first_visit AS first_visit,
        bounds.last_visit AS last_visit
FROM
    (SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
            MIN(TbFollowUp.FddVisit) AS first_visit,
            MAX(TbFollowUp.FddVisit) AS last_visit
    FROM TbFollowUP
    WHERE TbFollowUP.FddVisit < #{limit_date}#
    GROUP BY TbFollowUp.FdxReferencePatient) AS bounds
INNER JOIN TbFollowUp
    ON TbFollowUp.FdxReferencePatient = bounds.patient_idx
        AND TbFollowUp.FddVisit = bounds.last_visit
'''

### Subquery that get for each patient the last visit and the max next ###
### visit recorded for the previous period ###
PREVIOUS_VISIT_BOUNDS = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        TbFollowUp.FddVisitNext AS previous_last_next_visit,
        previous_bounds.previous_last_visit AS previous_last_visit
FROM
    (SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
            MAX(TbFollowUp.FddVisit) AS previous_last_visit
    FROM TbFollowUP
    WHERE TbFollowUP.FddVisit < #{previous_limit_date}#
    GROUP BY TbFollowUp.FdxReferencePatient) AS previous_bounds
INNER JOIN TbFollowUp
    ON TbFollowUp.FdxReferencePatient = previous_bounds.patient_idx
        AND TbFollowUp.FddVisit = previous_bounds.previous_last_visit
'''

### Subquery that get the last CD4 examination result of all patients ###
LAST_CD4 = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        MAX(TbFollowUp.FddExamen) AS last_cd4
FROM TbFollowUp
WHERE TbFollowUp.FddVisit < #{limit_date}#
    AND TbFollowUp.FdnLymphocyteCD4 IS NOT NULL
GROUP BY TbFollowUp.FdxReferencePatient
'''

### Subquery that get the last CV examination result of all patients ###
LAST_CV = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        MAX(TbFollowUp.FddExamen) AS last_cv
FROM TbFollowUp
WHERE TbFollowUp.FddVisit < #{limit_date}#
    AND TbFollowUp.FdnHIVLoad IS NOT NULL
GROUP BY TbFollowUp.FdxReferencePatient
'''

### Subquery that get the last diagnosed Tb of all patients ###
LAST_TB = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        MAX(TbFollowUp.FddVisit) AS last_tb
FROM (TbFollowUp
LEFT JOIN TbFollowUpDiagnosis
    ON TbFollowUp.FdxReference = TbFollowUpDiagnosis.FdxReferenceFollowUp)
LEFT JOIN TbReference
    ON TbFollowUpDiagnosis.FdxReferenceDiagnosis = TbReference.FdxReference
WHERE TbReference.FdnValue IN ({tb_diagnosis})
    AND TbFollowUp.FddVisit < #{limit_date}#
GROUP BY TbFollowUp.FdxReferencePatient
'''

### Subquery that get the last visit of all patients with prescribed ###
### cotrimoxazole ###
MAX_VISIT_CTX = \
'''
SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
        MAX(TbFollowUp.FddVisit) as max_visit_ctx
FROM (TbFollowUp
LEFT JOIN TbFollowUpDrug
    ON TbFollowUp.FdxReference = TbFollowUpDrug.FdxReferenceFollowUp)
LEFT JOIN TbReference
    ON TbFollowUpDrug.FdxReferenceDrug = TbReference.FdxReference
WHERE TbReference.FdnValue IN({ctx})
    AND TbFollowUp.FddVisit < #{limit_date}#
GROUP BY TbFollowUp.FdxReferencePatient
'''

### Final query used to get the table with all the necessary informations ###
FINAL_QUERY = \
'''
SELECT *
FROM (((((((({patients}) AS patients
LEFT JOIN ({min_patient_drug}) AS min_patient_drug
    ON patients.idx = min_patient_drug.patient_idx)
LEFT JOIN ({min_visit_drug}) AS min_visit_drug
    ON patients.idx = min_visit_drug.patient_idx)
LEFT JOIN ({visit_bounds}) AS visit_bounds
    ON patients.idx = visit_bounds.patient_idx)
LEFT JOIN ({last_cd4}) AS last_cd4
    ON patients.idx = last_cd4.patient_idx)
LEFT JOIN ({last_cv}) AS last_cv
    ON patients.idx = last_cv.patient_idx)
LEFT JOIN ({last_tb}) AS last_tb
    ON patients.idx = last_tb.patient_idx)
LEFT JOIN ({max_visit_ctx}) AS max_visit_ctx
    ON patients.idx = max_visit_ctx.patient_idx)
LEFT JOIN ({previous_visit_bounds}) AS previous_visit_bounds
    ON patients.idx = previous_visit_bounds.patient_idx
WHERE first_visit IS NOT NULL
ORDER BY patients.patient_code
'''.format(**{'patients': PATIENTS,
              'min_patient_drug': MIN_PATIENT_DRUG,
              'min_visit_drug': MIN_VISIT_DRUG,
              'visit_bounds': VISIT_BOUNDS,
              'last_cd4': LAST_CD4,
              'last_cv': LAST_CV,
              'last_tb': LAST_TB,
              'max_visit_ctx': MAX_VISIT_CTX,
              'previous_visit_bounds': PREVIOUS_VISIT_BOUNDS, })


def queryPatientsTable(cursor, month, year, excluded_drugs, hiv_positive_key,
                       tb_diagnosis, ctx):
    '''
    Query a Fuchia database and return the table containing all the necessary
    informations for computing the medical monthly report.
    cursor -- A cursor on the Fuchia database.
    month -- The month of the period to consider.
    year -- The year of the period to consider.
    excluded_drugs -- The reference ids of drugs to exclude (not ARVs).
    hiv_positive_key -- The key representing a HIV+ status.
    tb_diagnosis -- The list of tb diagnosis reference ids.
    ctx -- The list of cotrimoxazole reference ids.
    '''
    delta = relativedelta(months=1)
    limit_date = utils.getFirstDayOfPeriod(month, year) + delta
    previous_limit_date = limit_date - delta
    if len(excluded_drugs) == 0:
        excluded_drugs = [-1, ]
    if len(tb_diagnosis) == 0:
        tb_diagnosis = [-1, ]
    if len(ctx) == 0:
        ctx = [-1, ]
    excluded_drugs_str = ','.join([str(i) for i in excluded_drugs])
    tb_diagnosis_str = ','.join([str(i) for i in tb_diagnosis])
    ctx_str = ','.join([str(i) for i in ctx])
    kargs = { 'hiv_positive': hiv_positive_key,
              'excluded_drugs': excluded_drugs_str,
              'limit_date': limit_date,
              'previous_limit_date': previous_limit_date,
              'tb_diagnosis': tb_diagnosis_str,
              'ctx': ctx_str, }
    cursor.execute(FINAL_QUERY.format(**kargs))
    return cursor.fetchall()


def prettyResultTable(patients_table):
    '''
    Give a pretty out of a patients result table.
    '''
    pretty_out = ''
    tab_width = 25
    header = '\t|'.join(constants.ATTRIBUTES).expandtabs(tab_width)
    s = len(header) * ['-', ]
    pretty_out += ''.join(s)
    pretty_out += '\n{}'.format(header)
    pretty_out += '\n{}'.format(''.join(s))
    for l in patients_table:
        s = list()
        for attr in constants.ATTRIBUTES:
            a = getattr(l, attr)
            if isinstance(a, datetime) or isinstance(a, date):
                s.append('/'.join([str(a.day), str(a.month), str(a.year)]))
            else:
                s.append(str(a))
        pretty_out += '\n{}'.format('\t|'.join(s).expandtabs(tab_width))
    return pretty_out


#===========================#
# ARV prescriptions queries #
#===========================#

### Subquery that get the arv history of the patients ###
ARV_ANTECEDENTS = \
'''
SELECT TbPatient.FdxReference as patient_idx,
        TbPatientDrug.FddBeginning as beginning,
        TbPatientDrug.FdnDuration as duration,
        TbPatientDrug.FddCreated as creation,
        TbPatientDrug.FdxReferenceDrug AS drug_ref,
        TbReference.FdsLookup as drug_label
FROM (TbPatient
LEFT JOIN TbPatientDrug
    ON TbPatient.FdxReference = TbPatientDrug.FdxReferencePatient)
LEFT JOIN TbReference
    ON TbPatientDrug.FdxReferenceDrug = TbReference.FdxReference
WHERE TbPatientDrug.FdxReferenceDrug IS NOT NULL
    AND TbReference.FdnValue NOT IN ({excluded_drugs})
    AND (TbPatientDrug.FddBeginning < #{limit_date}#
        OR TbPatientDrug.FddBeginning IS NULL)
'''

### Subquery that get the last arv prescriptions of the patients ###
LAST_ARV_PRESCRIPTIONS = \
'''
SELECT visit.FdxReferencePatient AS patient_idx,
        max_visit.max_visit_drug AS last_arv_prescription,
        visit.FddVisitNext AS last_arv_rdv,
        visit_drug.FdxReferenceDrug AS drug_ref,
        reference.FdsLookup AS drug_label,
        visit_drug.FdnPrescription AS prescription
FROM
    (((SELECT TbFollowUp.FdxReferencePatient AS patient_idx,
            MAX(TbFollowUp.FddVisit) as max_visit_drug
    FROM (TbFollowUp
    LEFT JOIN TbFollowUpDrug
        ON TbFollowUp.FdxReference = TbFollowUpDrug.FdxReferenceFollowUp)
    LEFT JOIN TbReference
        ON TbFollowUpDrug.FdxReferenceDrug = TbReference.FdxReference
    WHERE TbReference.FdnValue NOT IN({excluded_drugs})
        AND TbFollowUp.FddVisit < #{limit_date}#
    GROUP BY TbFollowUp.FdxReferencePatient) AS max_visit
INNER JOIN (TbFollowUp AS visit)
    ON visit.FdxReferencePatient = max_visit.patient_idx
        AND visit.FddVisit = max_visit.max_visit_drug)
LEFT JOIN (TbFollowUpDrug AS visit_drug)
    ON visit.FdxReference = visit_drug.FdxReferenceFollowUp)
LEFT JOIN (TbReference AS reference)
    ON visit_drug.FdxReferenceDrug = reference.FdxReference
WHERE visit_drug.FdxReferenceDrug IS NOT NULL
    AND reference.FdnValue NOT IN({excluded_drugs})
    AND visit.FddVisit < #{limit_date}#
'''


def queryArvAntecedents(cursor, month, year, excluded_drugs):
    '''
    Query a Fuchia database and return a table containing the ARV antecedents
    of the patients recorded until the given period.
    cursor -- A cursor on the Fuchia database.
    month -- The month of the period to consider.
    year -- The year of the period to consider.
    excluded_drugs -- The reference ids of drugs to exclude (not ARVs).
    '''
    delta = relativedelta(months=1)
    limit_date = utils.getFirstDayOfPeriod(month, year) + delta
    if len(excluded_drugs) == 0:
        excluded_drugs = [-1, ]
    excluded_drugs_str = ','.join([str(i) for i in excluded_drugs])
    kargs = { 'excluded_drugs': excluded_drugs_str,
              'limit_date': limit_date, }
    cursor.execute(ARV_ANTECEDENTS.format(**kargs))
    return cursor.fetchall()

def queryLastArvPrescriptions(cursor, month, year, excluded_drugs):
    '''
    Query a Fuchia database and return a table containing the last ARV 
    prescriptions of the patients recorded until the given period.
    cursor -- A cursor on the Fuchia database.
    month -- The month of the period to consider.
    year -- The year of the period to consider.
    excluded_drugs -- The reference ids of drugs to exclude (not ARVs).
    '''
    delta = relativedelta(months=1)
    limit_date = utils.getFirstDayOfPeriod(month, year) + delta
    if len(excluded_drugs) == 0:
        excluded_drugs = [-1, ]
    excluded_drugs_str = ','.join([str(i) for i in excluded_drugs])
    kargs = { 'excluded_drugs': excluded_drugs_str,
              'limit_date': limit_date, }
    cursor.execute(LAST_ARV_PRESCRIPTIONS.format(**kargs))
    return cursor.fetchall()
