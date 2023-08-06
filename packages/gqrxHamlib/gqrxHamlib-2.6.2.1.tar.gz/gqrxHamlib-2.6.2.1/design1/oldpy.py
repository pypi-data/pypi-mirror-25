# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design1.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_actionOptions(object):
    def setupUi(self, actionOptions):
        actionOptions.setObjectName(_fromUtf8("actionOptions"))
        actionOptions.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(actionOptions)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.checkBox = QtGui.QCheckBox(actionOptions)
        self.checkBox.setGeometry(QtCore.QRect(10, 180, 371, 16))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.lineEdit = QtGui.QLineEdit(actionOptions)
        self.lineEdit.setGeometry(QtCore.QRect(110, 30, 113, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(actionOptions)
        self.label.setGeometry(QtCore.QRect(20, 40, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_2 = QtGui.QLineEdit(actionOptions)
        self.lineEdit_2.setGeometry(QtCore.QRect(110, 60, 113, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_2 = QtGui.QLabel(actionOptions)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_3 = QtGui.QLineEdit(actionOptions)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 90, 113, 27))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_3 = QtGui.QLabel(actionOptions)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_4 = QtGui.QLineEdit(actionOptions)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 200, 113, 27))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.label_4 = QtGui.QLabel(actionOptions)
        self.label_4.setGeometry(QtCore.QRect(10, 210, 61, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(actionOptions)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), actionOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), actionOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(actionOptions)

    def retranslateUi(self, actionOptions):
        actionOptions.setWindowTitle(_translate("actionOptions", "Dialog", None))
        self.checkBox.setText(_translate("actionOptions", "Pass frequency to fldigi (fldigi must be compiled including xmlrpc support)", None))
        self.label.setText(_translate("actionOptions", "IP address", None))
        self.label_2.setText(_translate("actionOptions", "gqrx port", None))
        self.label_3.setText(_translate("actionOptions", "Hamlib port", None))
        self.label_4.setText(_translate("actionOptions", "fldigi port", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    actionOptions = QtGui.QDialog()
    ui = Ui_actionOptions()
    ui.setupUi(actionOptions)
    actionOptions.show()
    sys.exit(app.exec_())

