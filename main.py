# -*- coding: utf-8 -*

# Copyright 2017 Solthis.
#
# This file is part of Fugen 2.0.
#
# Fugen 2.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fugen 2.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fugen 2.0. If not, see <http://www.gnu.org/licenses/>.


"""
Main module.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

import sys

from PySide.QtGui import QApplication
from PySide.QtCore import QTranslator

from gui.mainwindow import MainWindow
import constants
import utils
import texts


if __name__ == '__main__':

    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load(constants.QM_PATH)
    app.installTranslator(translator)

    mainwindow = MainWindow()

    def excepthook(excType, excValue, tracebackobj):
        msg_box = utils.getCriticalMessageBox(texts.GENERAL_ERROR_TITLE,
                                              texts.GENERAL_ERROR_MSG)
        msg_box.exec_()
        app.exit()

    sys.excepthook = excepthook

    try:
        from data.indicators.aggregation_indicators import *
        load_aggregation_operators()
        mainwindow.showMaximized()
        app.exec_()
    except AggregationIndicatorsError:
        t = "Impossible de charger les indicateurs agrégés"
        m = """
            Assurez vous d'avoir correctement configuré les indicateurs
            agrégés. Si le problème persiste, contactez Solthis.
            """
        msg_box = utils.getCriticalMessageBox(t, m)
        msg_box.exec_()
    except KeyboardInterrupt:
        pass
    except:
        t = "Une erreur est survenue pendant le démarrage du programme"
        m = """
            Assurez vous d'avoir correctement configuré l'outil, si le
            problème persiste, contactez Solthis.
            """
        msg_box = utils.getCriticalMessageBox(t, m)
        msg_box.exec_()
