from PyQt5 import QtCore, QtGui, QtWidgets
import json
import sys
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 900)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 50, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(50, 100, 450, 300))
        self.listView_2 = QtWidgets.QListWidget(self)
        self.listView_2.setGeometry(QtCore.QRect(50, 500, 450, 300))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(600, 100, 131, 41))
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(50, 450, 250, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 500, 131, 41))
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 575, 131, 41))
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(600, 825, 131, 41))
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Connected Clients:"))
        self.pushButton.setText(_translate("MainWindow", "1:1 Chat"))
        self.pushButton.setDisabled(True)
        self.label_2.setText(_translate("MainWindow", "Chat Rooms (Group Chat):"))
        self.pushButton_2.setText(_translate("MainWindow", "Create"))
        self.pushButton_3.setText(_translate("MainWindow", "Join"))
        self.pushButton_3.setDisabled(True)
        self.pushButton_4.setText(_translate("MainWindow", "Close"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())