# -*- coding: utf-8 -*

"""
Constants...
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

import sys
from os import path, environ, makedirs
from configparser import ConfigParser
import codecs


APPLICATION_TITLE = "Fugen 2.0"

if sys.platform == 'win32':
    appdata = path.join(environ['APPDATA'], APPLICATION_TITLE)
else:
    appdata = path.expanduser(path.join("~", "." + APPLICATION_TITLE))

if not path.exists(appdata):
    makedirs(appdata)

PATH = path.abspath(__file__)

#CONFIG = 'resources/config.ini'
CONFIG = path.join(path.dirname(PATH), 'resources', 'config.ini')
PARAMS = path.join(appdata, 'settings.ini')

config = ConfigParser()
try:
    with codecs.open(CONFIG, 'r', encoding='utf-8') as f:
        config.read_file(f)
except:
    pass

params = ConfigParser()
if path.exists(PARAMS):
    try:
        with codecs.open(PARAMS, 'r', encoding='utf-8') as f:
            params.read_file(f)
    except:
        pass
else:
    try:
        with codecs.open(PARAMS, 'a+', encoding='utf-8') as configfile:
            params.write(configfile)
    except:
        pass


try:
    def_params = params['DEFAULT']
except:
    def_params = None

try:
    def_config = config['DEFAULT']
except:
    def_config = None

ACCESS_DRIVER = 'Microsoft Access Driver (*.mdb)'
DB_FILTER_WINDOWS = 'Base Access (*.mdb)'
DB_FILTER_LINUX = 'Base sqlite (*.sqlite)'
ACCESS_EXT = '.mdb'
SQLITE_EXT = '.sqlite'
XLSX_FILTER = 'Fichier Excel (*.xlsx)'

try:
    ADMIN_PASSWORD = def_config['admin_password']
except:
    ADMIN_PASSWORD = 'fugen_admin_powers'

try:
    FUCHIADB_PASSWORD = def_config['database_password']
except:
    FUCHIADB_PASSWORD = '4598613458745961'

try:
    PDV_MONTHS_DELAY = int(def_params['lost_month_delay'])
except:
    PDV_MONTHS_DELAY = 3

try:
    DEFAULT_NEXT_VISIT_OFFSET = int(def_params['default_next_visit_offset'])
except:
    DEFAULT_NEXT_VISIT_OFFSET = 1

DEFAULT_AGE = 20

try:
    EXCLUDED_DRUGS = [int(n)
                      for n in def_params['excluded_arv_drugs'].split(',')]
except:
    EXCLUDED_DRUGS = [51, 52, 53, 54, 148, 149, 150, 151, 236, 297, 298, 299]

#  Correspond to TbFollowUpDrug.FdnPrescription,
#  refers to TbReference.FdnValue for FdsGroup == 'TDRG'
try:
    DRUG_RECEIVED = [int(n)
                      for n in def_params['drug_received'].split(',')]
except:
    DRUG_RECEIVED = [0, 1, 2, 3]

#  Correspond to TbFollowUpDrug.FdnPrescription,
#  refers to TbReference.FdnValue for FdsGroup == 'TDRG'
try:
    DRUG_STOPPED = [int(n)
                      for n in def_params['drug_stopped'].split(',')]
except:
    DRUG_STOPPED = [4, 5, 6, 7, 8, 9, 10, 11]

#  Correspond to TbFollowUpDrug.FdnPrescription,
#  refers to TbReference.FdnValue for FdsGroup == 'TDRG'
try:
    DRUG_RESTARTED = [int(n)
                      for n in def_params['drug_restarted'].split(',')]
except:
    DRUG_RESTARTED = [3, ]

try:
    HIV_POSITIVE = int(def_config['hiv_positive'])
except:
    HIV_POSITIVE = 1

try:
    TB_ENTRY = [int(n) for n in def_params['tb_entry'].split(',')]
except:
    TB_ENTRY = [2, ]

try:
    TB_DIAGNOSIS = [int(n) for n in def_params['tb_diagnosis'].split(',')]
except:
    TB_DIAGNOSIS = [12, 26, 74, ]

try:
    TB_KEYWORDS = [int(n) for n in def_params['tb_keywords'].split(',')]
except:
    TB_KEYWORDS = []

try:
    TB_RESEARCH_NS = def_params['tb_research_ns']
except:
    TB_RESEARCH_NS = 99

try:
    HEPATITIS_B_DIAGNOSIS = [int(n) for n in def_params['hepatitis_b_diagnosis'].split(',')]
except:
    HEPATITIS_B_DIAGNOSIS = []

try:
    HEPATITIS_B_KEYWORDS = [int(n) for n in def_params['hepatitis_b_keywords'].split(',')]
except:
    HEPATITIS_B_KEYWORDS = ['HEPATITE B', ]

try:
    CTX = [int(n) for n in def_params['ctx_drugs'].split(',')]
except:
    CTX = [51, 148, 236]

try:
    YEAR_UNIT = int(def_config['year_unit'])
except:
    YEAR_UNIT = 3

try:
    MONTH_UNIT = int(def_config['month_unit'])
except:
    MONTH_UNIT = 2

try:
    DAY_UNIT = int(def_config['day_unit'])
except:
    DAY_UNIT = 1

try:
    MALE = int(def_config['male'])
except:
    MALE = 0

try:
    FEMALE = int(def_config['female'])
except:
    FEMALE = 1

try:
    NOT_SPECIFIED = int(def_config['not_specified'])
except:
    NOT_SPECIFIED = 99

try:
    DEFAULT_DATABASE = def_params['default_database']
except:
    DEFAULT_DATABASE = ''

try:
    DEFAULT_SITENAME = def_params['default_sitename']
except:
    DEFAULT_SITENAME = ''

try:
    DEFAULT_REGION_NAME = def_params['default_region_name']
except:
    DEFAULT_REGION_NAME = ''

try:
    allow = int(def_config['allow_pdv_delay_modification'])
    ALLOW_PDV_DELAY_MODIF = bool(allow)
except:
    ALLOW_PDV_DELAY_MODIF = False


def setDefaultDatabase(default_db):
    params['DEFAULT']['default_database'] = default_db
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setDefaultSiteName(default_sn):
    params['DEFAULT']['default_sitename'] = default_sn
    global DEFAULT_SITENAME
    DEFAULT_SITENAME = default_sn
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setDefaultRegionName(default_rn):
    params['DEFAULT']['default_region_name'] = default_rn
    global DEFAULT_REGION_NAME
    DEFAULT_REGION_NAME = default_rn
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setPdvMonthDelay(delay):
    params['DEFAULT']['lost_month_delay'] = str(delay)
    global PDV_MONTHS_DELAY
    PDV_MONTHS_DELAY = delay
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setDefaultVisitOffset(offset):
    params['DEFAULT']['default_next_visit_offset'] = str(offset)
    global DEFAULT_NEXT_VISIT_OFFSET
    DEFAULT_NEXT_VISIT_OFFSET = offset
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setNonArvDrugs(str_list):
    params['DEFAULT']['excluded_arv_drugs'] = ','.join(str_list)
    global EXCLUDED_DRUGS
    EXCLUDED_DRUGS = [int(s) for s in str_list]
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setCtxDrugs(str_list):
    params['DEFAULT']['ctx_drugs'] = ','.join(str_list)
    global CTX
    CTX = [int(s) for s in str_list]
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setTbEntries(str_list):
    params['DEFAULT']['tb_entry'] = ','.join(str_list)
    global TB_ENTRY
    TB_ENTRY = [int(s) for s in str_list]
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)

def setTbDiagnosis(str_list):
    params['DEFAULT']['tb_diagnosis'] = ','.join(str_list)
    global TB_DIAGNOSIS
    TB_DIAGNOSIS = [int(s) for s in str_list]
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)


#==================================#
# Patients table attribute aliases #
#==================================#

IDX = 'idx'
PATIENT_CODE = 'patient_code'
HIV = 'hiv'
GENDER = 'gender'
AGE = 'age'
AGE_UNIT = 'age_unit'
AGE_DATE = 'age_date'
BIRTH_DATE = 'birth_date'
TRANSFERED = 'transfered'
DECENTRALIZED = 'decentralized'
DEAD = 'dead'
ENTRY_MODE = 'entry_mode'
ENTRY_MODE_LOOKUP = 'entry_mode_lookup'
CREATED_PATIENT_DRUG = 'created_patient_drug'
MIN_PATIENT_DRUG = 'min_patient_drug'
MIN_VISIT_DRUG = 'min_visit_drug'
FIRST_VISIT = 'first_visit'
LAST_VISIT = 'last_visit'
LAST_NEXT_VISIT = 'last_next_visit'
PREVIOUS_LAST_VISIT = 'previous_last_visit'
PREVIOUS_LAST_NEXT_VISIT = 'previous_last_next_visit'
LAST_CD4 = 'last_cd4'
LAST_CV = 'last_cv'
LAST_TB = 'last_tb'
MAX_VISIT_CTX = 'max_visit_ctx'

ATTRIBUTES = [IDX, PATIENT_CODE, GENDER, AGE, AGE_UNIT, AGE_DATE, BIRTH_DATE,
              TRANSFERED, DECENTRALIZED, DEAD, ENTRY_MODE,
              CREATED_PATIENT_DRUG, MIN_PATIENT_DRUG, MIN_VISIT_DRUG,
              FIRST_VISIT, LAST_VISIT, LAST_NEXT_VISIT, PREVIOUS_LAST_VISIT,
              PREVIOUS_LAST_NEXT_VISIT, LAST_CD4, LAST_CV, LAST_TB,
              MAX_VISIT_CTX, ]


#=================================#
# Prescriptions attributes aliase #
#=================================#

PATIENT_IDX = 'patient_idx'
BEGINNING = 'beginning'
DURATION = 'duration'
CREATION = 'creation'
DRUG_REF = 'drug_ref'
DRUG_LABEL = 'drug_label'
LAST_ARV_PRESC = 'last_arv_prescription'
LAST_ARV_RDV = 'last_arv_rdv'
PRESCRIPTION = 'prescription'


#===========#
# Gui icons #
#===========#

try:
    i = config['ICONS']
except:
    i = None

try:
    APP_ICON = i['app_icon']
except:
    APP_ICON = 'resources/icons/solthis.png'

try:
    EXPORT_XLSX_ICON = i['export_xlsx_icon']
except:
    EXPORT_XLSX_ICON = 'resources/icons/excel_export_icon.png'

try:
    GENERATE_ICON = i['generate_icon']
except:
    GENERATE_ICON = 'resources/icons/generate_report.png'

try:
    SETTINGS_ICON = i['settings_icon']
except:
    SETTINGS_ICON = 'resources/icons/settings_icon.png'

try:
    DETAILS_ICON = i['details_icon']
except:
    DETAILS_ICON = 'resources/icons/details_icon.png'

try:
    PRESCRIPTIONS_ICON = i['prescriptions_icon']
except:
    PRESCRIPTIONS_ICON = 'resources/icons/prescriptions_icon.png'

try:
    DATABASE_ICON = i['database_icon']
except:
    DATABASE_ICON = 'resources/icons/database_icon.png'

try:
    FUGEN_LOGO = i['fugen_logo']
except:
    FUGEN_LOGO = 'resources/about/logo_fugen.png'

try:
    SOLTHIS_LOGO = i['solthis_logo']
except:
    SOLTHIS_LOGO = 'resources/about/logo_solthis.png'

try:
    PNPCSP_LOGO = i['pnpcsp_logo']
except:
    PNPCSP_LOGO = 'resources/about/logo_pnpcsp.png'

try:
    CNLS_LOGO = i['cnls_logo']
except:
    CNLS_LOGO = 'resources/about/logo_cnls.png'

try:
    BANNER_LEFT = i['banner_left']
except:
    BANNER_LEFT = 'resources/banner/banner_left.png'

try:
    BANNER_RIGHT = i['banner_right']
except:
    BANNER_RIGHT = 'resources/banner/banner_right.png'

DEFAULT_REPORT_TEMPLATE = 'resources/report_template.xlsx'

try:
    REPORT_TEMPLATE = def_config['report_template']
except:
    REPORT_TEMPLATE = DEFAULT_REPORT_TEMPLATE


def set_report_template(report_xlsx):
    params['DEFAULT']['report_template'] = str(report_xlsx)
    global REPORT_TEMPLATE
    REPORT_TEMPLATE = report_xlsx
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)


DEFAULT_AGGREGATION_INDICATORS = 'resources/aggregation_indicators.json'

try:
    AGGREGATION_INDICATORS = def_config['aggregation_indicators']
except:
    AGGREGATION_INDICATORS = DEFAULT_AGGREGATION_INDICATORS


def set_aggregation_indicators(json_path):
    params['DEFAULT']['aggregation_indicators'] = str(json_path)
    global AGGREGATION_INDICATORS
    AGGREGATION_INDICATORS = json_path
    with codecs.open(PARAMS, 'w+', encoding='utf-8') as configfile:
        params.write(configfile)


try:
    QM_PATH = def_config['qm_fr']
except:
    QM_PATH = 'resources/qt_fr.qm'
