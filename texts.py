# -*- coding: utf-8 -*

'''
Texts of the GUI...

@author: Dimitri Justeau <dimitri.justeau@gmail.com>
'''

from os import path
from configparser import ConfigParser
import codecs


PATH = path.abspath(__file__)

TEXTS = 'resources/texts.ini'
# TEXTS = path.join(path.dirname(PATH), 'resources', 'texts.ini')

texts = ConfigParser()
try:
    with codecs.open(TEXTS, 'r', encoding='utf-8') as f:
        texts.readfp(f)
except:
    pass


#===================#
# Attributes header #
#===================#

try:
    h = texts['TABLE_HEADERS']
    ATTRIBUTES_GUI_LABELS = \
    [ h['idx'], h['patient_code'], h['gender'], h['age'], h['age_unit'],
      h['age_date'], h['birth_date'], h['transfered'], h['decentralized'],
      h['dead'], h['entry_mode'], h['created_patient_drug'],
      h['min_patient_drug'], h['min_visit_drug'], h['first_visit'],
      h['last_visit'], h['last_next_visit'], h['previous_last_visit'],
      h['previous_last_next_visit'], h['last_cd4'], h['last_cv'],
      h['last_tb'], h['max_visit_ctx'], ]
except:
    ATTRIBUTES_GUI_LABELS = \
    [ 'id', 'Code patient', 'Sexe', 'Age', "Unité", "Date de l'âge",
      'Date de naissance', 'Date transfert', 'Date décentralisation',
      'Date décès', "Mode d'entrée", "Antécédent ARV",
      "Date de l'antécédent ARV", "Première prescription ARV",
      "Première visite", "Dernière visite", "Dernier rendez-vous donné",
      "Avant-dernière visite", "Avant-dernier rendez-vous donné",
      "Dernier résultat CD4", "Dernière charge virale",
      "Dernière tuberculose diagnostiquée",
      "Dernière prescription de cotrimoxazole", ]


#====================#
# Gui Error Messages #
#====================#

try:
    e = texts['ERRORS']
except:
    e = None

try:
    EXPORT_ERROR_TITLE = e['export_error_title']
except:
    EXPORT_ERROR_TITLE = 'Export impossible'

try:
    EXPORT_ERROR_MSG = e['export_error_msg']
except:
    EXPORT_ERROR_MSG = "Une erreur est survenue pendant l'export du rapport,\
 assurez vous que le fichier n'est pas déjà ouvert, et  d'avoir bien \
configuré l'outil."

try:
    GENERATE_ERROR_TITLE = e['generate_error_title']
except:
    GENERATE_ERROR_TITLE = "Calcul du rapport impossible."

try:
    GENERATE_ERROR_MSG = e['generate_error_msg']
except:
    GENERATE_ERROR_MSG = "Le calcul du rapport est impossible, assurez-vous \
d'avoir selectionné une base de données Fuchia valide, et d'avoir bien \
configuré l'outil."

try:
    GENERAL_ERROR_TITLE = e['general_error_title']
except:
    GENERAL_ERROR_TITLE = "Une erreur est survenue"

try:
    GENERAL_ERROR_MSG = e['general_error_msg']
except:
    GENERAL_ERROR_MSG = "Une erreur est survenue pendant l'execution de \
l'application, la fenêtre va fermer. Contacter Solthis pour signaler \
ce problème."


#===========#
# GUI Texts #
#===========#

try:
    g = texts['GENERAL']
except:
    g = None

try:
    GENERATE_PROGRESS_DIAL = g['generate_progress_dial']
except:
    GENERATE_PROGRESS_DIAL = "Le calcul du rapport est en cours..."

try:
    EXPORT_XLSX_TXT = g['export_xlsx_txt']
except:
    EXPORT_XLSX_TXT = "Exporter le rapport vers Excel"

try:
    GENERATE_TXT = g['generate_txt']
except:
    GENERATE_TXT = "Générer le rapport"

try:
    FA_REPARTITION = g['fa_repartition']
except:
    FA_REPARTITION = "Répartition de la file active par traitement"

try:
    PRESC_REPARTITION = g['presc_repartition']
except:
    PRESC_REPARTITION = "Répartition des prescriptions par traitement"

try:
    PERIOD_LABEL = g['period_label']
except:
    PERIOD_LABEL = '<b>Période:<\b>'

try:
    TREATMENT = g['treatment']
except:
    TREATMENT = 'Traitement'

try:
    PATIENTS_NB = g['patients_nb']
except:
    PATIENTS_NB = 'Nombre de patients'

try:
    UPDATING_GUI = g['updating_gui']
except:
    UPDATING_GUI = "Mise à jour de l'interface..."

try:
    LOADING_DATA = g['loading_data']
except:
    LOADING_DATA = 'Chargement des données...'

try:
    COMPUTING_INDICATORS = g['computing_indicators']
except:
    COMPUTING_INDICATORS = 'Calcul des indicateurs...'

try:
    TOTAL = g['total']
except:
    TOTAL = 'Total:'

try:
    YEARS = g['years']
except:
    YEARS = 'Années'

try:
    MONTHS = g['months']
except:
    MONTHS = 'Mois'

try:
    DAYS = g['days']
except:
    DAYS = 'Jours'

try:
    MALE_TXT = g['male_txt']
except:
    MALE_TXT = 'Masculin'

try:
    FEMALE_TXT = g['female_txt']
except:
    FEMALE_TXT = 'Féminin'

try:
    SHOW_ADVANCED = g['show_advanced']
except:
    SHOW_ADVANCED = 'Montrer les paramètres avancés'

try:
    HIDE_ADVANCED = g['hide_advanced']
except:
    HIDE_ADVANCED = 'Cacher les paramètres avancés'

try:
    MODIFY_NON_ARV = g['modify_non_arv']
except:
    MODIFY_NON_ARV = "Modifier la liste des codes médicaments non ARV"

try:
    MODIFY_CTX = g['modify_ctx']
except:
    MODIFY_CTX = "Modifier la liste des codes médicaments cotrimoxazole"

try:
    MODIFY_TB_ENTRY = g['modify_tb_entry']
except:
    MODIFY_TB_ENTRY = "Modifier la liste des codes entrée Tb"

try:
    MODIFY_TB_DIAG = g['modify_tb_diag']
except:
    MODIFY_TB_DIAG = "Modifier la liste des codes diagnostic Tb"

try:
    SELECT_DB = g['select_db']
except:
    SELECT_DB = "Selectionner la base Fuchia à inspecter"

try:
    CHANGE_SITENAME = g['change_sitename']
except:
    CHANGE_SITENAME = "Changer le nom du site"

try:
    SITENAME_LABEL = g['sitename_label']
except:
    SITENAME_LABEL = "Nom du site"

try:
    MENU_FILE = g['menu_file']
except:
    MENU_FILE = 'Fichier'

try:
    MENU_WINDOW = g['menu_window']
except:
    MENU_WINDOW = 'Fenêtre'

try:
    MENU_HELP = g['menu_about']
except:
    MENU_HELP = 'Aide'

try:
    ACTION_ABOUT = g['action_about']
except:
    ACTION_ABOUT = 'À propos...'

try:
    TEXT_ABOUT = g['text_about']
except:
    TEXT_ABOUT = "<h3>Fugen</h3>\
<p>Fugen est un outil qui permet de générer des rapports mensuels de prise \
en charge du VIH à partir d'une base de données saisie dans le logiciel \
Fuchia. Cette version de Fugen a été adaptée au format de rapport en vigueur \
dans la République de Guinée.</p>"

try:
    CREDIT_ABOUT = g['credit_about']
except:
    CREDIT_ABOUT = "<i>Développé par Solthis, en partenariat avec\
 le PNPCSP  et le CNLS</i>"

try:
    MODIFY_ADVANCED_TITLE = g['modify_advanced_title']
except:
    MODIFY_ADVANCED_TITLE = 'Modifier les paramètres avancés'

try:
    MODIFY_ADVANCED_TEXT = g['modify_advanced_text']
except:
    MODIFY_ADVANCED_TEXT = 'Attention, avant de modifier les paramètres \
avancés, assurez-vous de savoir ce que vous faites, un mauvais paramètrage \
conduira à un calcul des rapports incorrect.'
