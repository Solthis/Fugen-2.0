# -*- coding: utf-8 -*

"""
Module used for computing the medical monthly report.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

from datetime import date
import time

from dateutil.relativedelta import relativedelta
import pandas as pd

import constants
from reports.medical import indicators
import reports.medical.query as medical_query
import utils
import texts


class MedicalReportGenerator(object):
    """
    Object instantiated with a cursor on a Fuchia database that can proceed
    the computation of the medical monthly report, and get several useful
    information such as the lost patients for a given period.
    """

    def __init__(self, cursor):
        self._cursor = cursor
        self._compute_time = 0
        self._indicators = dict()
        self._patients = dict()
        self._patients_table = list()
        self._arv_antecedents = dict()
        self._last_arv_prescriptions = dict()
        self._prescriptions_rep = dict()
        self._arv_fa_rep = dict()

    def reset(self):
        self._patients_table = list()
        self._compute_time = 0
        self._indicators = dict()
        self._patients = dict()
        self._arv_antecedents = dict()
        self._last_arv_prescriptions = dict()
        self._prescriptions_rep = dict()
        self._arv_fa_rep = dict()

    @property
    def cursor(self):
        """
        The cursor on the Fuchia database.
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        self._cursor = value
        self.reset()

    @property
    def indicators(self):
        """
        The last computed medical monthly report indicators.
        """
        return self._indicators

    @property
    def patients(self):
        """
        The codes of the patients according to the categories they
        correspond to.
        """
        return self._patients

    @property
    def data_table(self):
        """
        The raw data table queried from the database.
        """
        return self._patients_table

    @property
    def arv_antecedents(self):
        """
        The arv antecedents of the patients (dict of lists).
        """
        return self._arv_antecedents

    @property
    def last_arv_prescriptions(self):
        """
        The last arv prescriptions of the patients (dict of lists).
        """
        return self._last_arv_prescriptions

    @property
    def arv_prescriptions_repartition(self):
        """
        Repartition by ARV treatment of ARV prescriptions of the last
        computed period.
        """
        return self._prescriptions_rep

    @property
    def arv_active_file_repartition(self):
        """
        Repartition of the last computed active file by ARV treatment.
        """
        return self._arv_fa_rep

    @property
    def compute_time(self):
        """
        The last computing time.
        """
        return self._compute_time

    def _computeArvAntecedents(self, month, year):
        """
        Compute the arv antecedents.
        """
        data = medical_query.queryArvAntecedents(
            self.cursor,
            month,
            year,
            constants.EXCLUDED_DRUGS
        )
        for i, row in data.iterrows():
            patient_idx = getattr(row, constants.PATIENT_IDX)
            if patient_idx not in self.arv_antecedents:
                self.arv_antecedents[patient_idx] = [row, ]
            else:
                self.arv_antecedents[patient_idx].append(row)

    def _computeLastArvPrescription(self, month, year):
        """
        Compute the arv antecedents.
        """
        excl_drugs = constants.EXCLUDED_DRUGS
        data = medical_query.queryLastArvPrescriptions(
            self.cursor,
            month,
            year,
            excl_drugs
        )
        for i, row in data.iterrows():
            patient_idx = getattr(row, constants.PATIENT_IDX)
            if patient_idx not in self.last_arv_prescriptions:
                self.last_arv_prescriptions[patient_idx] = [row, ]
            else:
                self.last_arv_prescriptions[patient_idx].append(row)

    def computeMedicalReport(self, month, year, progress=None):
        """
        Compute the medical report and update the attributes for a given
        period.
        month -- The month of the period to consider.
        year -- The year of the period to consider.
        """
        # Reset the attributes
        start_time = time.time()
        self.reset()
        # Update progress
        steps = 0
        if progress is not None:
            progress.setLabelText(texts.LOADING_DATA)
            steps += 1
            progress.setValue(steps)
        # Initialize all indicators to zero
        for cat in indicators.INDICATOR_CATEGORY_KEYS:
            self.indicators[cat] = dict()
            self.patients[cat] = dict()
            for indic in indicators.INDICATOR_TYPE_KEYS:
                self.indicators[cat][indic] = 0
                self.patients[cat][indic] = list()
        # Compute ARV antecedents and last prescriptions
        self._computeArvAntecedents(month, year)
        self._computeLastArvPrescription(month, year)
        # Query the patient table
        table = medical_query.queryPatientsTable(
            self.cursor,
            month, year,
            constants.EXCLUDED_DRUGS,
            constants.HIV_POSITIVE,
            constants.TB_DIAGNOSIS,
            constants.CTX
        )
        self._patients_table = table
        if progress is not None:
            progress.setMaximum(len(self._patients_table) + 3)
            progress.setLabelText(texts.COMPUTING_INDICATORS)
        # Count loop
        for i, patient in self._patients_table.iterrows():
            category = _getCategoryOfPatient(patient, month, year)
            under_ARV = _isUnderARV(patient)
            followed = True
            code = getattr(patient, constants.PATIENT_CODE)
            # E7 - Incoming transfers
            if _isArvIncomingTransfer(patient, month, year):
                self.indicators[category][indicators.E7] += 1
                self.patients[category][indicators.E7].append(code)
            # E1 - New ARV patients
            elif _isNewInARV(patient, month, year):
                self.indicators[category][indicators.E1] += 1
                self.patients[category][indicators.E1].append(code)
                # E6 - Tb -> ARV
                if _isTbEntry(patient):
                    self.indicators[category][indicators.E6] += 1
                    self.patients[category][indicators.E6].append(code)
            # E3 - Dead patients
            if _isDead(patient, month, year):
                followed = False
                if under_ARV and _isDeadDuringPeriod(patient, month, year):
                    self.indicators[category][indicators.E3] += 1
                    self.patients[category][indicators.E3].append(code)
            # E4 - Transfered patients
            if followed and _isTransfered(patient, month, year):
                followed = False
                t = _isTransferedDuringPeriod(patient, month, year)
                if under_ARV and t:
                    self.indicators[category][indicators.E4] += 1
                    self.patients[category][indicators.E4].append(code)
            # E5 - Lost patients
            if followed and _isLost(patient, month, year):
                followed = False
                if under_ARV and _isLostDuringPeriod(patient, month, year):
                    self.indicators[category][indicators.E5] += 1
                    self.patients[category][indicators.E5].append(code)
            # E2 - Lost ARV patients back in the treatment
            not_lost = (not _isLost(patient, month, year)
                        or _isDeadDuringPeriod(patient, month, year)
                        or _isTransferedDuringPeriod(patient, month, year))
            if under_ARV and not_lost:
                if _wasPreviouslyLost(patient, month, year):
                    self.indicators[category][indicators.E2] += 1
                    self.patients[category][indicators.E2].append(code)
            # A1 - Tb diagnosed
            if _hadTbDiagnosedDuringPeriod(patient, month, year):
                self.indicators[category][indicators.A1] += 1
                self.patients[category][indicators.A1].append(code)
            # A2 - CD4 results
            if _hadCD4ResultDuringPeriod(patient, month, year):
                self.indicators[category][indicators.A2] += 1
                self.patients[category][indicators.A2].append(code)
            # A3 - CV results
            if _hadCVResultDuringPeriod(patient, month, year):
                self.indicators[category][indicators.A3] += 1
                self.patients[category][indicators.A3].append(code)
            if followed:
                # A4 - Patients receiving cotrimoxazole
                if _isUnderCtx(patient, month, year):
                    self.indicators[category][indicators.A4] += 1
                    self.patients[category][indicators.A4].append(code)
                # S1 - Under ARV since 12 months
                if  _isUnderArvSince12Months(patient, month, year):
                    self.indicators[category][indicators.S1] += 1
                    self.patients[category][indicators.S1].append(code)
                # S2 - Under ARV since 24 months
                if _isUnderArvSince24Months(patient, month, year):
                    self.indicators[category][indicators.S2] += 1
                    self.patients[category][indicators.S2].append(code)
                # S3 - Under ARV since 36 months
                if _isUnderArvSince36Months(patient, month, year):
                    self.indicators[category][indicators.S3] += 1
                    self.patients[category][indicators.S3].append(code)
                # S4 - Under ARV since 48 months
                if _isUnderArvSince48Months(patient, month, year):
                    self.indicators[category][indicators.S4] += 1
                    self.patients[category][indicators.S4].append(code)
                # B1 - Active file
                if under_ARV:
                    self.indicators[category][indicators.B1] += 1
                    self.patients[category][indicators.B1].append(code)
                    self.updatePrescriptionsDate(patient, month, year)
                # B2 - Total followed
                self.indicators[category][indicators.B2] += 1
                self.patients[category][indicators.B2].append(code)
            if progress is not None:
                steps += 1
                progress.setValue(steps)
        self._compute_time = time.time() - start_time

    def updatePrescriptionsDate(self, patient, month, year):
        """
        Update the arv prescription repartition and active file repartition
        with the given patient.
        """
        idx = getattr(patient, constants.IDX)
        drg_list = None
        presc_date = None
        presc_next_rdv = None
        if idx in self.last_arv_prescriptions:
            drg_list = self.last_arv_prescriptions[idx]
            presc_date = getattr(drg_list[0], constants.LAST_ARV_PRESC)
            presc_next_rdv = getattr(drg_list[0], constants.LAST_ARV_RDV)
        else:
            drg_list = self.arv_antecedents[idx]
        drg_labels = [getattr(drg, constants.DRUG_LABEL) for drg in drg_list]
        drg_key = frozenset(drg_labels)
        if drg_key not in self.arv_active_file_repartition:
            self.arv_active_file_repartition[drg_key] = 1
        else:
            self.arv_active_file_repartition[drg_key] += 1
        if presc_date is not None:
            m = presc_date.month
            y = presc_date.year
            if presc_next_rdv is None:
                d = relativedelta(months=constants.DEFAULT_NEXT_VISIT_OFFSET)
                presc_next_rdv = presc_date + d
            rdv_lim = utils.getLastDayOfPeriod(month, year)
            if (m == month and y == year) or presc_next_rdv.date() > rdv_lim:
                if drg_key not in self.arv_prescriptions_repartition:
                    self.arv_prescriptions_repartition[drg_key] = 1
                else:
                    self.arv_prescriptions_repartition[drg_key] += 1


# ============================== #
# Utility methods on patient row #
# ============================== #

def _getAgeOfPatient(patient, month, year):
    bdate = getattr(patient, constants.BIRTH_DATE)
    age_in_days = constants.DEFAULT_AGE * 365
    if not pd.isnull(bdate):
        age_in_days = (utils.getLastDayOfPeriod(month, year) -
                       date(bdate.year, bdate.month, bdate.day)).days
    else:
        age = getattr(patient, constants.AGE)
        age_unit = getattr(patient, constants.AGE_UNIT)
        age_date = getattr(patient, constants.AGE_DATE)
        if age is not None and age_date is not None and age_unit is not None:
            if age_unit == constants.MONTH_UNIT:
                age_in_days = age * 30
            elif age_unit == constants.YEAR_UNIT:
                age_in_days = age * 365
    return age_in_days // 365


def _getCategoryOfPatient(patient, month, year):
    gender = getattr(patient, constants.GENDER)
    age = _getAgeOfPatient(patient, month, year)
    if gender == constants.MALE:
        if age >= 15:
            return indicators.MA
        else:
            return indicators.MC
    else:
        if age >= 15:
            return indicators.FA
        else:
            return indicators.FC


def _getArvStartOfPatient(patient):
    """
    Give information on the ARV start of the patient.
    If the patient had started an ARV treatment, the start date is returned
    if available, else True is returned. If the patient hadn't started any
    ARV treatment, False is returned.
    patient -- The patient row to inspect.
    """
    # Case 1 - The patient already had an ARV treatment before being followed
    #           up in the center
    if getattr(patient, constants.CREATED_PATIENT_DRUG) is not None:
        min_patient_drug = getattr(patient, constants.MIN_PATIENT_DRUG)
        if min_patient_drug is None:
            # Case 1-a We don't have the date, True is returned
            return True
        else:
            # Case 1-b We have the date, it is returned
            return min_patient_drug.date()
    else:
        min_visit_drug = getattr(patient, constants.MIN_VISIT_DRUG)
        # Case 2 - The patient had started an ARV treatment in the center
        if min_visit_drug is not None:
            return min_visit_drug.date()
        else:
            # Case 3 - The patient hadn't started any ARV treatment
            return False


def _isUnderARV(patient):
    """
    Return True if the patient is under ARV.
    """
    arv_start = _getArvStartOfPatient(patient)
    if isinstance(patient, date):
        return True
    elif arv_start:
        return True
    return False


def _isNewInARV(patient, month, year):
    """
    Return True if the patient is new in ARV treatment for the given period.
    """
    arv_start = _getArvStartOfPatient(patient)
    if isinstance(arv_start, date):
        m = arv_start.month
        y = arv_start.year
        if y == year and m == month:
            return True
    return False


def _isArvIncomingTransfer(patient, month, year):
    """
    Return True if the patient is an under ARV incoming transfer.
    """
    first_visit = getattr(patient, constants.FIRST_VISIT)
    m = first_visit.month
    y = first_visit.year
    if m == month and y == year:
        previous_arv = getattr(patient, constants.CREATED_PATIENT_DRUG)
        arv_start = _getArvStartOfPatient(patient)
        if previous_arv is not None:
            if isinstance(arv_start, date):
                if arv_start <= utils.getLastDayOfPeriod(month, year):
                    return True
            elif arv_start:
                return True
    return False


def _isDead(patient, month, year):
    """
    If a patient is dead at a given period, return the date of death,
    if the patient is not dead, return False.
    """
    dead = getattr(patient, constants.DEAD)
    if not pd.isnull(dead) and dead.date() <= utils.getLastDayOfPeriod(month,
                                                                       year):
        return dead.date()
    return False


def _isDeadDuringPeriod(patient, month, year):
    """
    Return True if the patient is dead during the given period.
    """
    dead = _isDead(patient, month, year)
    if isinstance(dead, date):
        m = dead.month
        y = dead.year
        if y == year and m == month:
            return True
    return False


def _isTransfered(patient, month, year):
    """
    If a patient is transfered (or decentralized) at a given period,
    return the corresponding date, if the patient is not transfered
    (or decentralized), return False.
    """
    transfered = getattr(patient, constants.TRANSFERED)
    last_day = utils.getLastDayOfPeriod(month, year)
    if transfered is not None and transfered.date() <= last_day:
        return transfered.date()
    decentralized = getattr(patient, constants.DECENTRALIZED)
    if decentralized is not None and decentralized.date() <= last_day:
        return decentralized.date()
    return False


def _isTransferedDuringPeriod(patient, month, year):
    """
    Return True if the patient had been transfered (or decentralized) during
    the given period.
    """
    transfered = _isTransfered(patient, month, year)
    if isinstance(transfered, date):
        m = transfered.month
        y = transfered.year
        if y == year and m == month:
            return True
    return False


def _isLost(patient, month, year):
    """
    If a patient is lost, return the date when it was considered lost,
    if the patient is not lost, return False.
    """
    max_next_visit = getattr(patient, constants.LAST_NEXT_VISIT)
    if pd.isnull(max_next_visit):
        d = relativedelta(months=constants.DEFAULT_NEXT_VISIT_OFFSET)
        last_visit = getattr(patient, constants.LAST_VISIT)
        if pd.isnull(last_visit):
            msg = 'Error: There is no last visit for the patient {}'
            print(msg.format(patient))
        max_next_visit = last_visit + d
    delta = relativedelta(months=constants.PDV_MONTHS_DELAY)
    limit_date = utils.getLastDayOfPeriod(month, year)
    lost_date = max_next_visit.date() + delta
    if lost_date <= limit_date:
        return lost_date
    return False


def _wasPreviouslyLost(patient, month, year):
    """
    Return True if a patient was lost during the previous period of the
    given one.
    """
    prvs_max_next_visit = getattr(patient,
                                  constants.PREVIOUS_LAST_NEXT_VISIT)
    if prvs_max_next_visit is None:
        d = relativedelta(months=constants.DEFAULT_NEXT_VISIT_OFFSET)
        prvs_last_visit = getattr(patient, constants.PREVIOUS_LAST_VISIT)
        if prvs_last_visit is not None:
            prvs_max_next_visit = prvs_last_visit + d
    if prvs_max_next_visit is not None:
        delta = relativedelta(months=constants.PDV_MONTHS_DELAY)
        limit_date = (utils.getLastDayOfPeriod(month, year)
                     - relativedelta(months=1))
        lost_date = prvs_max_next_visit.date() + delta
        if lost_date <= limit_date:
            return True
    return False


def _isLostDuringPeriod(patient, month, year):
    """
    Return True if the patient was considered lost during the given period.
    """
    lost = _isLost(patient, month, year)
    if isinstance(lost, date):
        m = lost.month
        y = lost.year
        if y == year and m == month:
            return True
    return False


def _isTbEntry(patient):
    """
    Return True if the patient entry mode is Tb.
    """
    Tb = getattr(patient, constants.ENTRY_MODE)
    if Tb in constants.TB_ENTRY:
        return True
    return False


def _hadTbDiagnosedDuringPeriod(patient, month, year):
    """
    Return True if the patient a Tb diagnosed during the given period.
    """
    last_tb = getattr(patient, constants.LAST_TB)
    if last_tb is not None:
        m = last_tb.month
        y = last_tb.year
        if m == month and y == year:
            return True
    return False


def _hadCD4ResultDuringPeriod(patient, month, year):
    """
    Return True if the patient had a CD4 result during the given period.
    """
    cd4 = getattr(patient, constants.LAST_CD4)
    if cd4 is not None:
        m = cd4.month
        y = cd4.year
        if m == month and y == year:
            return True
    return False


def _hadCVResultDuringPeriod(patient, month, year):
    """
    Return True if the patient had a CV result during the given period.
    """
    cv = getattr(patient, constants.LAST_CV)
    if cv is not None:
        m = cv.month
        y = cv.year
        if m == month and y == year:
            return True
    return False


def _isUnderCtx(patient, month, year):
    """
    Return True if the patient is under cotrimoxazole.
    """
    ctx = getattr(patient, constants.MAX_VISIT_CTX)
    last_visit = getattr(patient, constants.LAST_VISIT)
    if ctx is not None and last_visit is not None:
        m_ctx = ctx.month
        y_ctx = ctx.year
        m_lv = last_visit.month
        y_lv = last_visit.year
        if m_ctx == m_lv and y_ctx == y_lv:
            lst_next_visit = getattr(patient, constants.LAST_NEXT_VISIT)
            if lst_next_visit is None:
                d = relativedelta(months=constants.DEFAULT_NEXT_VISIT_OFFSET)
                lst_next_visit = last_visit + d
            if lst_next_visit.date() > utils.getLastDayOfPeriod(month, year):
                return True
    return False


def _isUnderArvSince12Months(patient, month, year):
    """
    Return True if the patient is under ARV since exactly 12 months.
    """
    arv_start_date = _getArvStartOfPatient(patient)
    if isinstance(arv_start_date, date):
        m = arv_start_date.month
        y = arv_start_date.year
        if m == month and y == year - 1:
            return True
    return False


def _isUnderArvSince24Months(patient, month, year):
    """
    Return True if the patient is under ARV since exactly 24 months.
    """
    arv_start_date = _getArvStartOfPatient(patient)
    if isinstance(arv_start_date, date):
        m = arv_start_date.month
        y = arv_start_date.year
        if m == month and y == year - 2:
            return True
    return False


def _isUnderArvSince36Months(patient, month, year):
    """
    Return True if the patient is under ARV since exactly 36 months.
    """
    arv_start_date = _getArvStartOfPatient(patient)
    if isinstance(arv_start_date, date):
        m = arv_start_date.month
        y = arv_start_date.year
        if m == month and y == year - 3:
            return True
    return False


def _isUnderArvSince48Months(patient, month, year):
    """
    Return True if the patient is under ARV since exactly 48 months.
    """
    arv_start_date = _getArvStartOfPatient(patient)
    if isinstance(arv_start_date, date):
        m = arv_start_date.month
        y = arv_start_date.year
        if m == month and y == year - 4:
            return True
    return False


def prettyMedicalIndicators(indicators):
    """
    Give a pretty out of a medical indicators set.
    """
    pretty_out = ''
    width = 7
    cats = indicators.INDICATOR_CATEGORY_KEYS
    headers = '\t|'.join(['', ] + cats).expandtabs(width)
    h_lines = len(headers) * ['-', ]
    pretty_out += ''.join(h_lines)
    pretty_out += '\n{}'.format(headers)
    pretty_out += '\n{}'.format(''.join(h_lines))
    for e in indicators.E:
        line = [e, ] + [str(indicators[c][e]) for c in cats]
        pretty_out += '\n{}'.format('\t|'.join(line).expandtabs(width))
    pretty_out += '\n{}'.format(''.join(h_lines))
    for a in indicators.A:
        line = [a, ] + [str(indicators[c][a]) for c in cats]
        pretty_out += '\n{}'.format('\t|'.join(line).expandtabs(width))
    pretty_out += '\n{}'.format(''.join(h_lines))
    for s in indicators.S:
        line = [s, ] + [str(indicators[c][s]) for c in cats]
        pretty_out += '\n{}'.format('\t|'.join(line).expandtabs(width))
    pretty_out += '\n{}'.format(''.join(h_lines))
    for b in indicators.B:
        line = [b, ] + [str(indicators[c][b]) for c in cats]
        pretty_out += '\n{}'.format('\t|'.join(line).expandtabs(width))
    pretty_out += '\n{}'.format(''.join(h_lines))
    return pretty_out
