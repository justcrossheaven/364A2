from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QApplication
from invite import invite
import sys

class group_chat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 800)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 60, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(610, 60, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(610, 90, 161, 581))
        self.listView_2 = QtWidgets.QListWidget(self)
        self.listView_2.setGeometry(QtCore.QRect(30, 90, 501, 491))
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(30, 620, 361, 51))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(430, 620, 101, 51))
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 700, 161, 51))
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 700, 501, 51))
        self.retranslateUi()
        self.represented_name = 0
        self.invite = invite()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Roomnumber"))
        self.label_2.setText(_translate("Dialog", "Members"))
        self.pushButton.setText(_translate("Dialog", "Send"))
        self.pushButton_2.setText(_translate("Dialog", "Invite"))
        self.pushButton_3.setText(_translate("Dialog", "Close"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = group_chat()
    window.show()
    sys.exit(app.exec_())