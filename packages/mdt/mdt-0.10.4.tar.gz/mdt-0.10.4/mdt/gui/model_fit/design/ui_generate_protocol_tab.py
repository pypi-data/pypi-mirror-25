# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_protocol_tab.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GenerateProtocolTabContent(object):
    def setupUi(self, GenerateProtocolTabContent):
        GenerateProtocolTabContent.setObjectName("GenerateProtocolTabContent")
        GenerateProtocolTabContent.resize(827, 427)
        self.verticalLayout = QtWidgets.QVBoxLayout(GenerateProtocolTabContent)
        self.verticalLayout.setContentsMargins(-1, 11, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(GenerateProtocolTabContent)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(GenerateProtocolTabContent)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.line = QtWidgets.QFrame(GenerateProtocolTabContent)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.protocol_table = QtWidgets.QTableWidget(GenerateProtocolTabContent)
        self.protocol_table.setToolTip("")
        self.protocol_table.setRowCount(0)
        self.protocol_table.setColumnCount(0)
        self.protocol_table.setObjectName("protocol_table")
        self.verticalLayout.addWidget(self.protocol_table)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_18 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_6.addWidget(self.label_18)
        self.nmrShells = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.nmrShells.setObjectName("nmrShells")
        self.horizontalLayout_6.addWidget(self.nmrShells)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 3, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.nmrColumns = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.nmrColumns.setObjectName("nmrColumns")
        self.horizontalLayout_7.addWidget(self.nmrColumns)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 4, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_8 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_3.addWidget(self.label_8)
        self.nmrRows = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.nmrRows.setObjectName("nmrRows")
        self.horizontalLayout_3.addWidget(self.nmrRows)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_17 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_5.addWidget(self.label_17)
        self.nmrWeighted = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.nmrWeighted.setObjectName("nmrWeighted")
        self.horizontalLayout_5.addWidget(self.nmrWeighted)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_16 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_4.addWidget(self.label_16)
        self.nmrUnweighted = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.nmrUnweighted.setObjectName("nmrUnweighted")
        self.horizontalLayout_4.addWidget(self.nmrUnweighted)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_4 = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        self.differentShells = QtWidgets.QLabel(GenerateProtocolTabContent)
        self.differentShells.setWordWrap(True)
        self.differentShells.setObjectName("differentShells")
        self.horizontalLayout_9.addWidget(self.differentShells)
        self.horizontalLayout_9.setStretch(1, 1)
        self.gridLayout.addLayout(self.horizontalLayout_9, 1, 0, 1, 5)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_3 = QtWidgets.QFrame(GenerateProtocolTabContent)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadGB = QtWidgets.QPushButton(GenerateProtocolTabContent)
        self.loadGB.setObjectName("loadGB")
        self.horizontalLayout.addWidget(self.loadGB)
        self.loadProtocolButton = QtWidgets.QPushButton(GenerateProtocolTabContent)
        self.loadProtocolButton.setObjectName("loadProtocolButton")
        self.horizontalLayout.addWidget(self.loadProtocolButton)
        self.loadColumnButton = QtWidgets.QPushButton(GenerateProtocolTabContent)
        self.loadColumnButton.setObjectName("loadColumnButton")
        self.horizontalLayout.addWidget(self.loadColumnButton)
        self.saveButton = QtWidgets.QPushButton(GenerateProtocolTabContent)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.clearButton = QtWidgets.QPushButton(GenerateProtocolTabContent)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GenerateProtocolTabContent)
        QtCore.QMetaObject.connectSlotsByName(GenerateProtocolTabContent)

    def retranslateUi(self, GenerateProtocolTabContent):
        _translate = QtCore.QCoreApplication.translate
        GenerateProtocolTabContent.setWindowTitle(_translate("GenerateProtocolTabContent", "Form"))
        self.label.setText(_translate("GenerateProtocolTabContent", "Generate protocol file"))
        self.label_2.setText(_translate("GenerateProtocolTabContent", "Create a protocol file containing all your sequence information."))
        self.label_18.setText(_translate("GenerateProtocolTabContent", "# shells:"))
        self.nmrShells.setText(_translate("GenerateProtocolTabContent", "0"))
        self.label_13.setText(_translate("GenerateProtocolTabContent", "# columns:"))
        self.nmrColumns.setText(_translate("GenerateProtocolTabContent", "0"))
        self.label_8.setText(_translate("GenerateProtocolTabContent", "# rows:"))
        self.nmrRows.setText(_translate("GenerateProtocolTabContent", "0"))
        self.label_17.setText(_translate("GenerateProtocolTabContent", "# weighted:"))
        self.nmrWeighted.setText(_translate("GenerateProtocolTabContent", "0"))
        self.label_16.setText(_translate("GenerateProtocolTabContent", "# unweighted:"))
        self.nmrUnweighted.setText(_translate("GenerateProtocolTabContent", "0"))
        self.label_4.setText(_translate("GenerateProtocolTabContent", "Different shells:"))
        self.differentShells.setText(_translate("GenerateProtocolTabContent", "-"))
        self.loadGB.setText(_translate("GenerateProtocolTabContent", "Load g && b"))
        self.loadProtocolButton.setText(_translate("GenerateProtocolTabContent", "Load protocol"))
        self.loadColumnButton.setText(_translate("GenerateProtocolTabContent", "Add / Update column"))
        self.saveButton.setText(_translate("GenerateProtocolTabContent", "Save as"))
        self.clearButton.setText(_translate("GenerateProtocolTabContent", "Clear"))

