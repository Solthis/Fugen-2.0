# -*- coding: utf-8 -*

"""
Report consultation widget.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

from PySide.QtCore import *
from PySide.QtGui import *

from gui.ui.ui_reportwidget_view import Ui_ReportWidgetView
import reports.medical.indicators as medkeys


LEAF_STYLESHEET = \
    """
    QSpinBox {
        qproperty-maximum: 999999;\n
    }
    *[class=light] {
        background-color: rgb(255, 221, 139);
    }
    *[class=dark] {
        background-color: rgb(255, 211, 166);
    }
    *[class=header_light]{
        background-color: rgb(255, 202, 94);
    }
    *[class=header_dark]{
        background-color: rgb(245, 156, 66);
    }"""

AGGREGATED_STYLESHEET = \
    """
    QSpinBox {
        qproperty-maximum: 999999;\n
    }
    *[class=light] {
        background-color: #deebf7;
    }
    *[class=dark] {
        background-color: #c6dbef;
    }
    *[class=header_light]{
        background-color: #9ecae1;
    }
    *[class=header_dark]{
        background-color: #6baed6;
    }"""


class ReportViewWidget(QWidget, Ui_ReportWidgetView):
    '''
    Report edit/view widget.
    '''

    def __init__(self, indicators=None, parent=None):
        super(ReportViewWidget, self).__init__(parent)
        self.setupUi(self)
        self.aggregated = None
        self.indicators = None
        self.setIndicators(indicators)

    def setIndicators(self, indicators=None, aggregated=False):
        if aggregated != self.aggregated:
            self.aggregated = aggregated
            if self.aggregated:
                self.setStyleSheet(AGGREGATED_STYLESHEET)
            else:
                self.setStyleSheet(LEAF_STYLESHEET)
        self.indicators = indicators
        for cat in medkeys.INDICATOR_CATEGORY_KEYS:
            for indic in medkeys.INDICATOR_TYPE_KEYS:
                spin = getattr(self, '{0}{1}_spinbox'.format(indic, cat))
                if indicators is not None:
                    spin.setValue(indicators[cat][indic])
                    spin.setReadOnly(True)
                else:
                    spin.setValue(0)
