# coding: utf-8

from data.indicators.base_indicator import *
from data.indicators.active_list import *
from data.indicators.arv_restarted import *
from data.indicators.arv_retention import *
from data.indicators.arv_started_patients import *
from data.indicators.arv_stopped import *
from data.indicators.cd4 import *
from data.indicators.ctx import *
from data.indicators.dead_patients import *
from data.indicators.followed_patients import *
from data.indicators.hepatitis_diagnosis import *
from data.indicators.included_patients import *
from data.indicators.incoming_transfer_patients import *
from data.indicators.lost_back_patients import *
from data.indicators.lost_patients import *
from data.indicators.patient_indicator import *
from data.indicators.received_arv import *
from data.indicators.tb_arv_treatment import *
from data.indicators.tb_diagnosis import *
from data.indicators.tb_research import *
from data.indicators.tb_treatment import *
from data.indicators.tb_vih import *
from data.indicators.transferred_patients import *
from data.indicators.viral_load import *
from data.indicators.utility_indicators import *
from data.indicators.aggregation_indicators import *

aggregation_indicators = load_aggregation_operators()
