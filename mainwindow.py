# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowGhazNK.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(658, 586)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setObjectName(u"mainLayout")
        self.searchLayout = QHBoxLayout()
        self.searchLayout.setObjectName(u"searchLayout")
        self.searchTypeLayout = QHBoxLayout()
        self.searchTypeLayout.setObjectName(u"searchTypeLayout")
        self.searchTypeLabel = QLabel(Form)
        self.searchTypeLabel.setObjectName(u"searchTypeLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchTypeLabel.sizePolicy().hasHeightForWidth())
        self.searchTypeLabel.setSizePolicy(sizePolicy)

        self.searchTypeLayout.addWidget(self.searchTypeLabel)

        self.searchTypeComboBox = QComboBox(Form)
        self.searchTypeComboBox.addItem("")
        self.searchTypeComboBox.addItem("")
        self.searchTypeComboBox.setObjectName(u"searchTypeComboBox")

        self.searchTypeLayout.addWidget(self.searchTypeComboBox)


        self.searchLayout.addLayout(self.searchTypeLayout)

        self.searchMethodLayout = QHBoxLayout()
        self.searchMethodLayout.setObjectName(u"searchMethodLayout")
        self.searchMethodLabel = QLabel(Form)
        self.searchMethodLabel.setObjectName(u"searchMethodLabel")
        sizePolicy.setHeightForWidth(self.searchMethodLabel.sizePolicy().hasHeightForWidth())
        self.searchMethodLabel.setSizePolicy(sizePolicy)

        self.searchMethodLayout.addWidget(self.searchMethodLabel)

        self.searchMethodComboBox = QComboBox(Form)
        self.searchMethodComboBox.addItem("")
        self.searchMethodComboBox.addItem("")
        self.searchMethodComboBox.addItem("")
        self.searchMethodComboBox.setObjectName(u"searchMethodComboBox")

        self.searchMethodLayout.addWidget(self.searchMethodComboBox)

        self.searchMethodLayout.setStretch(1, 1)

        self.searchLayout.addLayout(self.searchMethodLayout)

        self.searchLayout.setStretch(0, 1)
        self.searchLayout.setStretch(1, 1)

        self.mainLayout.addLayout(self.searchLayout)

        self.fileInputLayout = QHBoxLayout()
        self.fileInputLayout.setObjectName(u"fileInputLayout")
        self.filePathLabel = QLabel(Form)
        self.filePathLabel.setObjectName(u"filePathLabel")

        self.fileInputLayout.addWidget(self.filePathLabel)

        self.filePathLineEdit = QLineEdit(Form)
        self.filePathLineEdit.setObjectName(u"filePathLineEdit")

        self.fileInputLayout.addWidget(self.filePathLineEdit)

        self.browseButton = QPushButton(Form)
        self.browseButton.setObjectName(u"browseButton")

        self.fileInputLayout.addWidget(self.browseButton)

        self.similarityLabel = QLabel(Form)
        self.similarityLabel.setObjectName(u"similarityLabel")

        self.fileInputLayout.addWidget(self.similarityLabel)

        self.similaritySpinBox = QSpinBox(Form)
        self.similaritySpinBox.setObjectName(u"similaritySpinBox")
        self.similaritySpinBox.setValue(50)

        self.fileInputLayout.addWidget(self.similaritySpinBox)

        self.searchButton = QPushButton(Form)
        self.searchButton.setObjectName(u"searchButton")

        self.fileInputLayout.addWidget(self.searchButton)


        self.mainLayout.addLayout(self.fileInputLayout)

        self.searchResultsGroupBox = QGroupBox(Form)
        self.searchResultsGroupBox.setObjectName(u"searchResultsGroupBox")
        self.horizontalLayout = QHBoxLayout(self.searchResultsGroupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.inputImageGraphicsView = QGraphicsView(self.searchResultsGroupBox)
        self.inputImageGraphicsView.setObjectName(u"inputImageGraphicsView")

        self.horizontalLayout.addWidget(self.inputImageGraphicsView)

        self.label = QLabel(self.searchResultsGroupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.inputRepresentation = QGraphicsView(self.searchResultsGroupBox)
        self.inputRepresentation.setObjectName(u"inputRepresentation")

        self.horizontalLayout.addWidget(self.inputRepresentation)

        self.histogramWidget = QWidget(self.searchResultsGroupBox)
        self.histogramWidget.setObjectName(u"histogramWidget")

        self.horizontalLayout.addWidget(self.histogramWidget)


        self.mainLayout.addWidget(self.searchResultsGroupBox)

        self.outputScrollArea = QScrollArea(Form)
        self.outputScrollArea.setObjectName(u"outputScrollArea")
        self.outputScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 636, 281))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.resultTable = QTableWidget(self.scrollAreaWidgetContents)
        if (self.resultTable.columnCount() < 3):
            self.resultTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.resultTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.resultTable.setObjectName(u"resultTable")

        self.verticalLayout_2.addWidget(self.resultTable)

        self.outputScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.mainLayout.addWidget(self.outputScrollArea)

        self.mainLayout.setStretch(0, 1)
        self.mainLayout.setStretch(1, 1)
        self.mainLayout.setStretch(2, 3)
        self.mainLayout.setStretch(3, 6)

        self.verticalLayout.addLayout(self.mainLayout)

        self.addToDataBaseButton = QPushButton(Form)
        self.addToDataBaseButton.setObjectName(u"addToDataBaseButton")

        self.verticalLayout.addWidget(self.addToDataBaseButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.searchTypeLabel.setText(QCoreApplication.translate("Form", u"Search method:", None))
        self.searchTypeComboBox.setItemText(0, QCoreApplication.translate("Form", u"Images", None))
        self.searchTypeComboBox.setItemText(1, QCoreApplication.translate("Form", u"Videos", None))

        self.searchMethodLabel.setText(QCoreApplication.translate("Form", u"Search method:", None))
        self.searchMethodComboBox.setItemText(0, QCoreApplication.translate("Form", u"Mean Color", None))
        self.searchMethodComboBox.setItemText(1, QCoreApplication.translate("Form", u"Histogram Similarity", None))
        self.searchMethodComboBox.setItemText(2, QCoreApplication.translate("Form", u"Color Layout", None))

        self.filePathLabel.setText(QCoreApplication.translate("Form", u"File path:", None))
        self.browseButton.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.similarityLabel.setText(QCoreApplication.translate("Form", u"Similarity constraint", None))
        self.similaritySpinBox.setSuffix(QCoreApplication.translate("Form", u"%", None))
        self.similaritySpinBox.setPrefix(QCoreApplication.translate("Form", u"\u2265", None))
        self.searchButton.setText(QCoreApplication.translate("Form", u"Search", None))
        self.searchResultsGroupBox.setTitle(QCoreApplication.translate("Form", u"Input Representation", None))
        self.label.setText(QCoreApplication.translate("Form", u"Mean Color:", None))
        ___qtablewidgetitem = self.resultTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Path", None));
        ___qtablewidgetitem1 = self.resultTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Similarity (%)", None));
        ___qtablewidgetitem2 = self.resultTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Preview", None));
        self.addToDataBaseButton.setText(QCoreApplication.translate("Form", u"Add to data base", None))
    # retranslateUi

