# -*- coding: utf-8 -*

"""
Main window of the tool.
@author: Dimitri Justeau <dimitri.justeau@gmail.com>
"""

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from re import split
import platform

from PySide.QtGui import *
from PySide.QtCore import *
import numpy as np

from gui.ui.ui_mainwindow import Ui_MainWindow
from gui.ui.ui_string_list_dialog import Ui_StringListDialog
from gui.report_widget import ReportWidget
from export import exportMedicalReportToExcel
import constants
import texts
import utils
from reports.medical import indicators as med_indics
from gui.ui.ui_about_dialog import Ui_AboutDialog
from template_processor.base_template_processor import BaseTemplateProcessor
from template_processor.xls_template_processor import XlsTemplateProcessor
from reports.medical.query_bis import *


class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    Mainwindow of the tool, build from the ui generated by pyside-uic
    from the corresponding .ui Qt Designer file.
    '''

    def __init__(self):
        '''
        Initialise the mainwindow, create the report widget and
        connect the signals.
        '''
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.addDockWidget(Qt.LeftDockWidgetArea,
                           self.prescriptions_dockwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea,
                            self.patients_details_dockwidget)
        self.setWindowIcon(QIcon(constants.APP_ICON))
        self.data_dockwidget.close()
        self.advanced_frame.hide()
        self.parameters_dockwidget.setMinimumHeight(0)
        self.parameters_dockwidget.setMinimumWidth(0)
        self.parameters_dockcontents.adjustSize()
        self.parameters_dockwidget.close()
        self.initParametersWidget()
        # self.initDataTable()
        self.parameters_dockwidget.setFloating(True)
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        self.central_widget = QMainWindow()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.site_label)
        vlayout.addWidget(self.scrollArea)
        cw = QWidget()
        cw.setLayout(vlayout)
        self.central_widget.setCentralWidget(cw)
        self.setCentralWidget(self.central_widget)
        self.initMainToolbar()
        self.initSecondaryToolbar()
        self.initMenuBar()
        self.setStatusTips()
        self.initPatientDetailsTreeWidget()
        self.initPrescriptionsTreeWidget()
        self.setWindowTitle(constants.APPLICATION_TITLE)
        self.export_xlsx.setEnabled(False)
        # Init the default date of the period date edit
        today = date.today()
        max_date = today - relativedelta(months=1)
        self.period_dateedit.setMaximumDate(max_date)
        self.period_dateedit.setDate(max_date)
        # Create the reports widget and add them to the scrollview

        self.cursor = utils.getCursor('mdb/CHA.sqlite', '')
        self.patients = query_patients_dataframe(self.cursor)
        self.visits = query_visits_dataframe(self.cursor)
        self.patient_drugs = query_patient_drugs_dataframe(self.cursor)
        self.visit_drugs = query_visit_drugs_dataframe(self.cursor)

        self.report_widget = ReportWidget()
        self.reportArea.layout().addWidget(self.report_widget)
        self.report_widget.hide()

        # Init progress dialog
        self.progress = QProgressDialog(str(), str(), 0, 100, self)
        self.progress.setCancelButton(None)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setWindowTitle("Calcul des indicateurs...")

        # Connect the signals
        self.connectSignals()
        self.modifyAdvancedClicked()

    def initMainToolbar(self):
        # Settings
        self.settings_action = self.parameters_dockwidget.toggleViewAction()
        self.settings_action.setIcon(QIcon(constants.SETTINGS_ICON))
        self.toolBar.addAction(self.settings_action)
        # Details
        self.details_action = \
            self.patients_details_dockwidget.toggleViewAction()
        self.details_action.setIcon(QIcon(constants.DETAILS_ICON))
        self.toolBar.addAction(self.details_action)
        # Prescriptions
        self.prescr_action = self.prescriptions_dockwidget.toggleViewAction()
        self.prescr_action.setIcon(QIcon(constants.PRESCRIPTIONS_ICON))
        self.toolBar.addAction(self.prescr_action)
        # Data table
        self.data_table_action = self.data_dockwidget.toggleViewAction()
        self.data_table_action.setIcon(QIcon(constants.DATABASE_ICON))
        self.toolBar.addAction(self.data_table_action)
        self.show_data_table = False
        self.data_table_action.setEnabled(False)

    def initSecondaryToolbar(self):
        self.toolbar2 = QToolBar()
        # Date edit
        w = QWidget()
        l = QHBoxLayout()
        l.setContentsMargins(0, 0, 10, 0)
        l.setSpacing(10)
        l.addWidget(QLabel(texts.PERIOD_LABEL))
        self.period_dateedit = QDateEdit()
        self.period_dateedit.setDisplayFormat('MM/yyyy')
        l.layout().addWidget(self.period_dateedit)
        w.setLayout(l)
        self.toolbar2.addWidget(w)
        # Generate
        gen_txt = texts.GENERATE_TXT
        self.action_generate = self.toolbar2.addAction(gen_txt)
        self.action_generate.setIcon(QIcon(constants.GENERATE_ICON))
        # Exports
        ww = QWidget()
        ww.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar2.addSeparator()
        self.toolbar2.addWidget(ww)
        self.export_xlsx = self.toolbar2.addAction(texts.EXPORT_XLSX_TXT)
        self.export_xlsx.setIcon(QIcon(constants.EXPORT_XLSX_ICON))
        self.toolbar2.addSeparator()
        self.central_widget.addToolBar(self.toolbar2)

    def initMenuBar(self):
        # Menu file
        self.filemenu = self.menubar.addMenu(texts.MENU_FILE)
        self.filemenu.addAction(texts.SELECT_DB, self.browseButtonClicked)
        self.filemenu.addAction(texts.CHANGE_SITENAME,
                                self.changeSiteNameClicked)
        # Menu window
        self.windowmenu = self.menubar.addMenu(texts.MENU_WINDOW)
        self.windowmenu.addAction(self.settings_action)
        self.windowmenu.addAction(self.details_action)
        self.windowmenu.addAction(self.prescr_action)
        self.windowmenu.addAction(self.data_table_action)
        # Menu about
        self.menuhelp = self.menubar.addMenu(texts.MENU_HELP)
        self.about_action = self.menuhelp.addAction(texts.ACTION_ABOUT,
                                                    self.showAboutDialog)

    def setStatusTips(self):
        self.export_xlsx.setStatusTip(self.export_xlsx.iconText())
        self.action_generate.setStatusTip(self.action_generate.iconText())
        self.settings_action.setStatusTip(self.settings_action.iconText())
        self.details_action.setStatusTip(self.details_action.iconText())
        t = self.data_table_action.iconText()
        self.data_table_action.setStatusTip(t)
        self.prescr_action.setStatusTip(self.prescr_action.iconText())

    def initPatientDetailsTreeWidget(self):
        self.treeWidget.setColumnCount(2)
        self.patients_details_root_items = dict()
        self.headers_buttons = dict()
        for indic in med_indics.INDICATOR_TYPE_KEYS:
            item = QTreeWidgetItem(self.treeWidget)
            item.setFirstColumnSpanned(True)
            button = CatPushButton(med_indics.INDICATORS_DESC[indic], item)
            self.patients_details_root_items[indic] = item
            self.headers_buttons[indic] = button
            self.treeWidget.setItemWidget(item, 0, button)

    def initPrescriptionsTreeWidget(self):
        # Treewidget
        self.arv_presc_treeWidget.setColumnCount(2)
        self.arv_presc_treeWidget.setHeaderLabels([texts.TREATMENT,
                                                   texts.PATIENTS_NB])
        # Active file repartition
        self.fa_repartition = QTreeWidgetItem(self.arv_presc_treeWidget)
        self.fa_repartition.setFirstColumnSpanned(True)
        t1 = texts.FA_REPARTITION
        self.fa_rep_button = CatPushButton(t1, self.fa_repartition)
        self.arv_presc_treeWidget.setItemWidget(self.fa_repartition, 0,
                                                self.fa_rep_button)
        # Prescriptions repartition
        self.presc_repartition = QTreeWidgetItem(self.arv_presc_treeWidget)
        self.presc_repartition.setFirstColumnSpanned(True)
        t2 = texts.PRESC_REPARTITION
        self.presc_rep_button = CatPushButton(t2, self.presc_repartition)
        self.arv_presc_treeWidget.setItemWidget(self.presc_repartition, 0,
                                                self.presc_rep_button)

    def initDataTable(self):
        '''
        Initialise the data table with header.
        '''
        c_count = len(texts.ATTRIBUTES_GUI_LABELS) - 1
        self.data_table.setColumnCount(c_count)
        hlabels = texts.ATTRIBUTES_GUI_LABELS[1:]
        self.data_table.setHorizontalHeaderLabels(hlabels)
        self.data_table.resizeColumnsToContents()

    def connectSignals(self):
        """
        Connect the signals to their corresponding slots.
        """
        # self.action_generate.triggered.connect(self.generateButtonClicked)
        self.action_generate.triggered.connect(self.generate_button_clicked)
        self.browse_button.clicked.connect(self.browseButtonClicked)
        self.export_xlsx.triggered.connect(self.exportReportToExcel)
        self.change_name_button.clicked.connect(self.changeSiteNameClicked)
        self.advanced_parameters_button.clicked \
            .connect(self.advancedParametersButtonClicked)
        self.pdv_delay_spin.valueChanged.connect(self.pdvDelaySpinChanged)
        self.default_visit_offset_spin.valueChanged \
            .connect(self.defaultVisitOffsetSpinChanged)
        self.modify_non_arv_button.clicked \
            .connect(self.modifyNonArvDrugsClicked)
        self.modify_ctx_button.clicked.connect(self.modifyCtxClicked)
        self.modify_entry_tb_button.clicked \
            .connect(self.modifyTbEntryClicked)
        self.modify_diag_tb_button.clicked.connect(self.modifyTbDiagClicked)
        self.show_table_checkbox.toggled.connect(self.showDataTableChanged)
        self.modify_advanced_pushbutton.toggled \
            .connect(self.modifyAdvancedClicked)

    def update_progress(self, progress):
        self.progress.setValue(progress)

    def generate_button_clicked(self):
        # Compute report
        tproc = XlsTemplateProcessor(
            constants.MEDICAL_REPORT_TEMPLATE,
            self.patients,
            self.visits,
            self.patient_drugs,
            self.visit_drugs
        )
        self.report_widget.template_processor = tproc
        self.report_widget.template_processor.update_progress.connect(
            self.update_progress
        )
        self.progress.setValue(0)
        self.progress.setMaximum(self.report_widget.cell_count())
        self.progress.setMinimumDuration(0)
        self.progress.forceShow()
        month = self.period_dateedit.date().month()
        year = self.period_dateedit.date().year()
        start_date = utils.getFirstDayOfPeriod(month, year)
        end_date = utils.getLastDayOfPeriod(month, year)
        self.report_widget.compute_values(
            start_date,
            end_date
        )
        self.report_widget.show()

    def updatePatientDetails(self):
        for indic in med_indics.INDICATOR_TYPE_KEYS:
            item = self.patients_details_root_items[indic]
            item.takeChildren()
            i = 0
            for cat in med_indics.INDICATOR_CATEGORY_KEYS:
                l = self.generator.patients[cat][indic]
                if len(l) == 0:
                    i += 1
                else:
                    self.headers_buttons[indic].setEnabled(True)
                    cat_item = QTreeWidgetItem(item)
                    cat_item.setFirstColumnSpanned(True)
                    t = med_indics.CATEGORIES_DESC[cat]
                    f = cat_item.font(0)
                    f.setBold(True)
                    cat_item.setFont(0, f)
                    cat_item.setText(0, t)
                    for code in l:
                        p_item = QTreeWidgetItem(cat_item)
                        p_item.setFirstColumnSpanned(True)
                        p_item.setText(0, code)
            if i == len(med_indics.INDICATOR_CATEGORY_KEYS):
                self.headers_buttons[indic].setEnabled(False)
            # Total
            total = QTreeWidgetItem(item)
            t = texts.TOTAL
            f = total.font(0)
            f.setBold(True)
            brush = QBrush(Qt.darkGray)
            total.setForeground(0, brush)
            total.setForeground(1, brush)
            total.setFont(0, f)
            total.setText(0, t)
            tot = sum([self.generator.indicators[c][indic]
                       for c in med_indics.INDICATOR_CATEGORY_KEYS])
            total.setText(1, str(tot))

    def updatePrescriptionsDetails(self):
        # Active file repartition
        self.fa_repartition.takeChildren()
        fa_items = self.generator.arv_active_file_repartition.items()
        sorted_fa = sorted(fa_items, key=lambda t: t[1], reverse=True)
        # Repartition
        for key, value in sorted_fa:
            line_item = QTreeWidgetItem(self.fa_repartition)
            t = ' / '.join(key)
            f = line_item.font(0)
            f.setBold(True)
            line_item.setFont(0, f)
            line_item.setText(0, t)
            line_item.setText(1, str(value))
        if len(fa_items) == 0:
            self.fa_rep_button.setEnabled(False)
        else:
            self.fa_rep_button.setEnabled(True)
        # Total
        total_fa = QTreeWidgetItem(self.fa_repartition)
        t = texts.TOTAL
        f = total_fa.font(0)
        f.setBold(True)
        brush = QBrush(Qt.darkGray)
        total_fa.setForeground(0, brush)
        total_fa.setForeground(1, brush)
        total_fa.setFont(0, f)
        total_fa.setText(0, t)
        tot = sum([i[1] for i in sorted_fa])
        total_fa.setText(1, str(tot))
        # Prescriptions repartion
        self.presc_repartition.takeChildren()
        presc_items = self.generator.arv_prescriptions_repartition.items()
        sorted_presc = sorted(presc_items, key=lambda t: t[1], reverse=True)
        # Repartition
        for key, value in sorted_presc:
            line_item = QTreeWidgetItem(self.presc_repartition)
            t = ' / '.join(key)
            f = line_item.font(0)
            f.setBold(True)
            line_item.setFont(0, f)
            line_item.setText(0, t)
            line_item.setText(1, str(value))
        # Total
        total_presc = QTreeWidgetItem(self.presc_repartition)
        t = texts.TOTAL
        f = total_presc.font(0)
        f.setBold(True)
        total_presc.setForeground(0, brush)
        total_presc.setForeground(1, brush)
        total_presc.setFont(0, f)
        total_presc.setText(0, t)
        tot = sum([i[1] for i in sorted_presc])
        total_presc.setText(1, str(tot))
        if len(fa_items) == 0:
            self.presc_rep_button.setEnabled(False)
        else:
            self.presc_rep_button.setEnabled(True)

    def updateDataTable(self):
        """
        Update the data table.
        """
        table = self.generator.data_table
        self.data_table.clearContents()
        self.data_table.setRowCount(len(table))
        for i, p in enumerate(table):
            for j in range(1, len(constants.ATTRIBUTES)):
                a = constants.ATTRIBUTES[j]
                if a == constants.ENTRY_MODE:
                    v = getattr(p, constants.ENTRY_MODE_LOOKUP)
                else:
                    v = getattr(p, a)
                    if a == constants.AGE_UNIT:
                        if v == constants.YEAR_UNIT:
                            v = texts.YEARS
                        elif v == constants.MONTH_UNIT:
                            v = texts.MONTHS
                        elif v == constants.DAY_UNIT:
                            v = texts.DAYS
                    elif a == constants.GENDER:
                        if v == constants.MALE:
                            v = texts.MALE_TXT
                        elif v == constants.FEMALE:
                            v = texts.FEMALE_TXT
                item = QTableWidgetItem(str(v))
                if isinstance(v, datetime):
                    v = v.date()
                    item = QTableWidgetItem(str(v))
                if v is None:
                    item = QTableWidgetItem()
                if a == constants.CREATED_PATIENT_DRUG:
                    if v:
                        item = QTableWidgetItem(True)
                        item.setCheckState(Qt.Checked)
                    else:
                        item = QTableWidgetItem(False)
                        item.setCheckState(Qt.Unchecked)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.data_table.setItem(i, j - 1, item)
        self.data_table.resizeColumnsToContents()

    def initParametersWidget(self):
        """
        Initialize the parameters widget with the stored values.
        """
        self.fuchiadb_path_lineedit.setText(constants.DEFAULT_DATABASE)
        self.site_nameedit.setText(constants.DEFAULT_SITENAME)
        self.pdv_delay_spin.setValue(constants.PDV_MONTHS_DELAY)
        offset_default = constants.DEFAULT_NEXT_VISIT_OFFSET
        self.default_visit_offset_spin.setValue(offset_default)
        non_arv_t = ','.join([str(i) for i in constants.EXCLUDED_DRUGS])
        self.non_arv_lineedit.setText(non_arv_t)
        ctx_t = ','.join([str(i) for i in constants.CTX])
        self.ctx_lineedit.setText(ctx_t)
        entry_tb_t = ','.join([str(i) for i in constants.TB_ENTRY])
        self.entry_tb_lineedit.setText(entry_tb_t)
        diag_tb = ','.join([str(i) for i in constants.TB_DIAGNOSIS])
        self.diag_tb_lineedit.setText(diag_tb)
        if constants.ALLOW_PDV_DELAY_MODIF:
            self.pdv_delay_spin.setEnabled(True)
        else:
            self.pdv_delay_spin.setEnabled(False)

    def advancedParametersButtonClicked(self):
        """
        Hide/Show the advanced parameters section when the button is clicked.
        """
        if self.advanced_frame.isVisible():
            self.advanced_frame.hide()
            t = texts.SHOW_ADVANCED
            self.advanced_parameters_button.setText(t)
        else:
            self.advanced_frame.show()
            t = texts.HIDE_ADVANCED
            self.advanced_parameters_button.setText(t)
        self.parameters_dockwidget.setMinimumHeight(0)
        self.parameters_dockwidget.setMinimumWidth(0)
        self.parameters_dockcontents.adjustSize()

    def pdvDelaySpinChanged(self):
        constants.setPdvMonthDelay(self.pdv_delay_spin.value())

    def defaultVisitOffsetSpinChanged(self):
        v = self.default_visit_offset_spin.value()
        constants.setDefaultVisitOffset(v)

    def modifyNonArvDrugsClicked(self):
        dialog = ModifyStrListDialog([str(i)
                                      for i in constants.EXCLUDED_DRUGS])
        wt = texts.MODIFY_NON_ARV
        dialog.setWindowTitle(wt)
        b = dialog.exec_()
        if b:
            str_list = dialog.model.stringList()
            constants.setNonArvDrugs(str_list)
            self.non_arv_lineedit.setText(','.join(str_list))

    def modifyCtxClicked(self):
        dialog = ModifyStrListDialog([str(i) for i in constants.CTX])
        wt = texts.MODIFY_CTX
        dialog.setWindowTitle(wt)
        b = dialog.exec_()
        if b:
            str_list = dialog.model.stringList()
            constants.setCtxDrugs(str_list)
            self.ctx_lineedit.setText(','.join(str_list))

    def modifyTbEntryClicked(self):
        dialog = ModifyStrListDialog([str(i) for i in constants.TB_ENTRY])
        dialog.setWindowTitle(texts.MODIFY_TB_ENTRY)
        b = dialog.exec_()
        if b:
            str_list = dialog.model.stringList()
            constants.setTbEntries(str_list)
            self.entry_tb_lineedit.setText(','.join(str_list))

    def modifyTbDiagClicked(self):
        dialog = ModifyStrListDialog([str(i)
                                      for i in constants.TB_DIAGNOSIS])
        dialog.setWindowTitle(texts.MODIFY_TB_DIAG)
        b = dialog.exec_()
        if b:
            str_list = dialog.model.stringList()
            constants.setTbDiagnosis(str_list)
            self.diag_tb_lineedit.setText(','.join(str_list))

    def showDataTableChanged(self):
        """
        Slot called when the show data table checkbox is changed. If checked
        the data table can be shown and will be updated when the report is
        generated, else the data table won't be showable, and won't be
        updated.
        """
        if self.show_table_checkbox.isChecked():
            self.show_data_table = True
            self.data_table_action.setEnabled(True)
        else:
            self.show_data_table = False
            self.data_table_action.setEnabled(False)
            self.data_dockwidget.close()

    def browseButtonClicked(self):
        """
        Slot called when the browse button is clicked.
        """
        t = texts.SELECT_DB
        db_filter = constants.DB_FILTER_WINDOWS
        if platform.system() == "Linux":
            db_filter = constants.DB_FILTER_LINUX
        filename = QFileDialog.getOpenFileName(None, t, filter=db_filter)
        if filename[0] != '':
            self.fuchiadb_path_lineedit.setText(filename[0])
            constants.setDefaultDatabase(filename[0])
            fname = split('/', filename[0])[-1]
            name = split(constants.ACCESS_EXT, fname)[0]
            constants.setDefaultSiteName(name)
            self.site_nameedit.setText(name)
            d = self.period_dateedit.date()
            sitetext = '{} - {}/{}'.format(name,
                                           d.month(),
                                           d.year())
            self.site_label.setText(sitetext)

    def changeSiteNameClicked(self):
        """
        Slot called when the change sitename button is clicked.
        """
        text = QInputDialog.getText(self, texts.CHANGE_SITENAME,
                                    texts.SITENAME_LABEL,
                                    QLineEdit.Normal,
                                    self.site_nameedit.text())
        if text[1]:
            self.site_nameedit.setText(text[0])
            constants.setDefaultSiteName(text[0])
            self.site_nameedit.setText(text[0])
            d = self.period_dateedit.date()
            sitetext = '{} - {}/{}'.format(text[0],
                                           d.month(),
                                           d.year())
            self.site_label.setText(sitetext)

    def exportReportToExcel(self):
        t = texts.EXPORT_XLSX_TXT
        filename = \
            QFileDialog.getSaveFileName(None,
                                        t,
                                        filter=constants.XLSX_FILTER)
        if filename[0] != '':
            try:
                month = self.period_dateedit.date().month()
                year = self.period_dateedit.date().year()
                indics = self.medicalreportwidget.indicators
                exportMedicalReportToExcel(self.site_nameedit.text(),
                                           month, year,
                                           indics, filename[0])
            except:
                t = texts.EXPORT_ERROR_TITLE
                m = texts.EXPORT_ERROR_MSG
                msg_box = utils.getCriticalMessageBox(t, m)
                msg_box.exec_()

    def generate(self, month, year, progress):
        try:
            cursor = utils.getCursor(self.fuchiadb_path_lineedit.text(),
                                     constants.FUCHIADB_PASSWORD)
            self.generator.cursor = cursor
            self.generator.computeMedicalReport(month, year, progress)
            return True
        except:
            progress.cancel()
            t = texts.GENERATE_ERROR_TITLE
            m = texts.GENERATE_ERROR_MSG
            msg_box = utils.getCriticalMessageBox(t, m)
            msg_box.exec_()
            return False

    def showAboutDialog(self):
        about = AboutDialog()
        about.exec_()

    def modifyAdvancedClicked(self):
        """
        Slot called when modify advanced parameters button is clicked,
        enable/disable the advanced parameters modification.
        """
        if self.modify_advanced_pushbutton.isChecked():
            c = QMessageBox.warning(self,
                                    texts.MODIFY_ADVANCED_TITLE,
                                    texts.MODIFY_ADVANCED_TEXT,
                                    QMessageBox.Ok | QMessageBox.Cancel)
            if c == QMessageBox.Ok:
                self.pdv_group.setEnabled(True)
                self.treatment_group.setEnabled(True)
                self.tb_group.setEnabled(True)
                self.misc_group.setEnabled(True)
            else:
                self.pdv_group.setEnabled(False)
                self.treatment_group.setEnabled(False)
                self.tb_group.setEnabled(False)
                self.misc_group.setEnabled(False)
                self.modify_advanced_pushbutton.setChecked(False)
        else:
            self.pdv_group.setEnabled(False)
            self.treatment_group.setEnabled(False)
            self.tb_group.setEnabled(False)
            self.misc_group.setEnabled(False)


class CatPushButton(QPushButton):
    """
    Button for the treewidgets main categories.
    """

    def __init__(self, text, item, parent=None):
        super(CatPushButton, self).__init__(text, parent)
        self.item = item
        self.clicked.connect(self.action)
        self.setEnabled(False)

    def action(self):
        self.item.setExpanded(not self.item.isExpanded())


class ModifyStrListDialog(QDialog, Ui_StringListDialog):
    """
    Dialog for modifying a list of string, used in the parameter widget.
    """

    def __init__(self, str_list, parent=None):
        super(ModifyStrListDialog, self).__init__(parent)
        self.setupUi(self)
        self.str_list = str_list
        self.model = QStringListModel(str_list)
        self.listView.setModel(self.model)
        s_model = self.listView.selectionModel()
        s_model.currentChanged.connect(self.currentChanged)
        self.delete_button.clicked.connect(self.deleteClicked)
        self.spinBox.valueChanged.connect(self.spinChanged)
        self.add_button.clicked.connect(self.addClicked)
        self.delete_button.setEnabled(False)
        self.listView.setCurrentIndex(QModelIndex())
        self.spinChanged()

    def currentChanged(self):
        index = self.listView.selectionModel().currentIndex()
        if index.isValid():
            self.delete_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)

    def deleteClicked(self):
        index = self.listView.selectionModel().currentIndex()
        self.model.removeRows(index.row(), 1)
        self.str_list = self.model.stringList()

    def addClicked(self):
        v = self.spinBox.value()
        self.model.insertRows(self.model.rowCount(), 1)
        i = self.model.index(self.model.rowCount() - 1, 0)
        self.model.setData(i, str(v))
        self.str_list = self.model.stringList()
        self.spinChanged()

    def spinChanged(self):
        v = self.spinBox.value()
        if str(v) in self.str_list:
            self.add_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)


class AboutDialog(QDialog, Ui_AboutDialog):
    """
    Dialog showing general informations about the software.
    """

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(texts.ACTION_ABOUT)
        self.fugendesc_label.setText(texts.TEXT_ABOUT)
        self.credit_label.setText(texts.CREDIT_ABOUT)
        self.fugenlogo_label.setPixmap(QPixmap(QImage(constants.FUGEN_LOGO)))
        solthis_pix = QPixmap(QImage(constants.SOLTHIS_LOGO))
        self.solthis_logo_label.setPixmap(solthis_pix)
        pnpcsp_pix = QPixmap(QImage(constants.PNPCSP_LOGO))
        self.pnpcsp_logo_label.setPixmap(pnpcsp_pix)
        cnls_pix = QPixmap(QImage(constants.CNLS_LOGO))
        self.cnls_logo_label.setPixmap(cnls_pix)
