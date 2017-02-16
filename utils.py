# -*- coding: utf-8 -*

'''
Module containing general purpose utility methods.

@author: Dimitri Justeau <dimitri.justeau@gmail.com>
'''

import sys
import traceback
from datetime import date
from calendar import monthrange

import pyodbc
from PySide.QtGui import QMessageBox, QSpacerItem

import constants


def getLastDayOfPeriod(month, year):
    '''
    Return the last day of the given period (month/year)
    '''
    return date(year, month, monthrange(year, month)[1])

def getFirstDayOfPeriod(month, year):
    '''
    Return the last day of the given period (month/year)
    '''
    return date(year, month, 1)

def getCursor(accessdb_path, password):
    '''
    Return a cursor on an MS Access database.
    accessdb_path -- The path of the Access file.
    password -- The password of the database.
    '''
    cnxn = pyodbc.connect('DRIVER={0};DBQ={1};PWD={2}'
                          .format(constants.ACCESS_DRIVER,
                                  accessdb_path,
                                  password))
    return cnxn.cursor()

def getCriticalMessageBox(text, informative_text, detailed_text=None):
    message_box = QMessageBox()
    h_spacer = QSpacerItem(500, 0)
    gl = message_box.layout()
    gl.addItem(h_spacer, gl.rowCount(), 0, 1, gl.columnCount())
    message_box.setWindowTitle(constants.APPLICATION_TITLE)
    message_box.addButton(QMessageBox.Ok)
    message_box.setText('<b>{}'.format(text))
    message_box.setInformativeText(informative_text)
    if detailed_text is not None:
        message_box.setDetailedText(detailed_text)
    else:
        excType, excValue, tracebackobj = sys.exc_info()
        tb_list = traceback.format_exception(excType,
                                             excValue,
                                             tracebackobj)
        tb_str = ''.join(tb_list)
        message_box.setDetailedText(tb_str)
    message_box.setIcon(QMessageBox.Critical)
    return message_box