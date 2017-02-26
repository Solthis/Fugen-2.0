# coding: utf-8

import pandas as pd

import constants
import utils


# The driver for accessing the Microsoft Access database #
ACCESS_DRIVER = constants.ACCESS_DRIVER

# The password of the Fuchia database #
FUCHIADB_PASSWORD = constants.FUCHIADB_PASSWORD


PATIENTS_SQL = \
    """
    SELECT TbPatient.FdxReference AS id,
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
    """


VISITS_SQL = \
    """
    SELECT TbFollowUp.FdxReference AS id,
        TbFollowUp.FdxReferencePatient AS patient_id,
        TbFollowUp.FddVisit AS visit_date,  /* Datetime */
        TbFollowUp.FddVisitNext AS next_visit_date,  /* Datetime */
        TbFollowUp.FddExamen AS examination_date,  /* Datetime */
        TbFollowUp.FdnLymphocyteCD4 AS cd4,
        TbFollowUp.FdnHIVLoad AS viral_load
    FROM TbFollowUp
    """


VISIT_DRUGS_SQL = \
    """
    SELECT TbFollowUpDrug.FdxReference AS id,
        TbFollowUpDrug.FdxReferenceFollowUp AS visit_id,
        TbFollowUpDrug.FdxReferenceDrug AS drug_id
    FROM TbFollowUpDrug
    """


PATIENT_DRUGS_SQL = \
    """
    SELECT TbPatientDrug.FdxReference AS id,
        TbPatientDrug.FdxReferencePatient AS patient_id,
        TbPatientDrug.FdxReferenceDrug AS drug_id,
        TbPatientDrug.FddBeginning AS beginning,  /* Datetime */
        TbPatientDrug.FdnDuration AS duration
    FROM TbPatientDrug
    """


def query_patients_dataframe(cursor):
    cursor.execute(PATIENTS_SQL)
    data = cursor.fetchall()
    df = pd.DataFrame.from_records(
        data,
        index='id',
        columns=(
            'id',
            'patient_code',
            'hiv',
            'gender',
            'age',
            'age_unit',
            'age_date',  # Datetime
            'birth_date',  # Datetime
            'transferred',  # Datetime
            'decentralized',  # Datetime
            'dead',  # Datetime
            'entry_mode',
            'entry_mode_lookup'
        )
    )
    df['age_date'] = df['age_date'].apply(utils.to_datetime)
    df['birth_date'] = df['birth_date'].apply(utils.to_datetime)
    df['transferred'] = df['transferred'].apply(utils.to_datetime)
    df['decentralized'] = df['decentralized'].apply(utils.to_datetime)
    df['dead'] = df['dead'].apply(utils.to_datetime)
    df = df.assign(id=df.index)
    return df


def query_visits_dataframe(cursor):
    cursor.execute(VISITS_SQL)
    data = cursor.fetchall()
    df = pd.DataFrame.from_records(
        data,
        index='id',
        columns=(
            'id',
            'patient_id',
            'visit_date',  # Datetime
            'next_visit_date',  # Datetime
            'examination_date',  # Datetime
            'cd4',
            'viral_load',
        )
    )
    df['visit_date'] = df['visit_date'].apply(utils.to_datetime)
    df['next_visit_date'] = df['next_visit_date'].apply(utils.to_datetime)
    df['examination_date'] = df['examination_date'].apply(utils.to_datetime)
    df = df.assign(id=df.index)
    return df


def query_visit_drugs_dataframe(cursor):
    cursor.execute(VISIT_DRUGS_SQL)
    data = cursor.fetchall()
    df = pd.DataFrame.from_records(
        data,
        index='id',
        columns=(
            'id',
            'visit_id',
            'drug_id'
        )
    )
    df = df.assign(id=df.index)
    return df


def query_patient_drugs_dataframe(cursor):
    cursor.execute(PATIENT_DRUGS_SQL)
    data = cursor.fetchall()
    df = pd.DataFrame.from_records(
        data,
        index='id',
        columns=(
            'id',
            'patient_id',
            'drug_id',
            'beginning',  # Datetime
            'duration'
        )
    )
    df['beginning'] = df['beginning'].apply(utils.to_datetime)
    df = df.assign(id=df.index)
    return df