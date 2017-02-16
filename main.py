# -*- coding: utf-8 -*

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

    mainwindow.showMaximized()
    app.exec_()
