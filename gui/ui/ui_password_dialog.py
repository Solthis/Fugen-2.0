# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/password_dialog.ui'
#
# Created: Thu Mar 30 11:42:44 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PassWordDialog(object):
    def setupUi(self, PassWordDialog):
        PassWordDialog.setObjectName("PassWordDialog")
        PassWordDialog.resize(399, 162)
        self.verticalLayout = QtGui.QVBoxLayout(PassWordDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(PassWordDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.password_line_edit = QtGui.QLineEdit(PassWordDialog)
        self.password_line_edit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_line_edit.setObjectName("password_line_edit")
        self.verticalLayout.addWidget(self.password_line_edit)
        self.error_label = QtGui.QLabel(PassWordDialog)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(143, 146, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.error_label.setPalette(palette)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.error_label.setFont(font)
        self.error_label.setText("")
        self.error_label.setWordWrap(True)
        self.error_label.setObjectName("error_label")
        self.verticalLayout.addWidget(self.error_label)
        self.buttonBox = QtGui.QDialogButtonBox(PassWordDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PassWordDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PassWordDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PassWordDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PassWordDialog)

    def retranslateUi(self, PassWordDialog):
        PassWordDialog.setWindowTitle(QtGui.QApplication.translate("PassWordDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PassWordDialog", "Pour modifier les paramètres avancés, veuillez saisir le mot de passe administrateur", None, QtGui.QApplication.UnicodeUTF8))

