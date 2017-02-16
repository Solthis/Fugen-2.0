# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'string_list_dialog.ui'
#
# Created: Fri Oct  3 16:54:01 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_StringListDialog(object):
    def setupUi(self, StringListDialog):
        StringListDialog.setObjectName("StringListDialog")
        StringListDialog.resize(294, 202)
        self.verticalLayout_2 = QtGui.QVBoxLayout(StringListDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listView = QtGui.QListView(StringListDialog)
        self.listView.setObjectName("listView")
        self.horizontalLayout_2.addWidget(self.listView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBox = QtGui.QSpinBox(StringListDialog)
        self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinBox.setMaximum(99999)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.add_button = QtGui.QPushButton(StringListDialog)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.delete_button = QtGui.QPushButton(StringListDialog)
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(StringListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(StringListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), StringListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), StringListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StringListDialog)

    def retranslateUi(self, StringListDialog):
        StringListDialog.setWindowTitle(QtGui.QApplication.translate("StringListDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.add_button.setText(QtGui.QApplication.translate("StringListDialog", "Ajouter", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("StringListDialog", "Supprimer", None, QtGui.QApplication.UnicodeUTF8))

