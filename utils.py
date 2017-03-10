# -*- coding: utf-8 -*

"""
Module containing general purpose utility methods.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

import sys
import traceback
import platform
import sqlite3
from datetime import date, datetime
from calendar import monthrange

import pyodbc
import pandas as pd
from PySide.QtGui import QMessageBox, QSpacerItem

import constants


def getLastDayOfPeriod(month, year):
    """
    Return the last day of the given period (month/year)
    """
    return datetime(
        year,
        month,
        monthrange(year, month)[1],
        hour=23,
        minute=59,
        second=59
    )


def getFirstDayOfPeriod(month, year):
    """
    Return the last day of the given period (month/year)
    """
    return datetime(
        year,
        month,
        1,
        hour=0,
        minute=0,
        second=0
    )


def get_date_str(date_value):
    if platform.system() == 'Windows':
        return "#{}#".format(date_value)
    elif platform.system() == 'Linux':
        return "date('{}')".format(date_value)


def to_datetime(d):
    if d in (None, ''):
        return pd.NaT
    try:
        return datetime.strptime(d, "%m/%d/%Y %H:%M:%S")
    except ValueError:
        return pd.NaT


def bunch_factory(cursor, row):
    d = lambda: None
    for idx, col in enumerate(cursor.description):
        setattr(d, col[0], row[idx])
    return d


def getCursor(db_path, password):
    """
    Return a cursor on an MS Access database (Or sqlite if on Linux).
    db_path -- The path of the Access file.
    password -- The password of the database.
    """
    if platform.system() == 'Linux':
        conn = sqlite3.connect(db_path)
        # conn.row_factory = bunch_factory
        return conn.cursor()
    db_string = 'DRIVER={0};DBQ={1};PWD={2}'.format(
        constants.ACCESS_DRIVER,
        db_path,
        password
    )
    cnxn = pyodbc.connect(db_string)
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
