# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plover_midi/gui_qt/midi_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MidiWidget(object):
    def setupUi(self, MidiWidget):
        MidiWidget.setObjectName("MidiWidget")
        MidiWidget.resize(176, 58)
        self.formLayout = QtWidgets.QFormLayout(MidiWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(MidiWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.port = QtWidgets.QComboBox(MidiWidget)
        self.port.setEditable(True)
        self.port.setObjectName("port")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.port)

        self.retranslateUi(MidiWidget)
        self.port.editTextChanged['QString'].connect(MidiWidget.on_port_changed)
        QtCore.QMetaObject.connectSlotsByName(MidiWidget)

    def retranslateUi(self, MidiWidget):

        MidiWidget.setWindowTitle(_("Form"))
        self.label.setText(_("Port"))

