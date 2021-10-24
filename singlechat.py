from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QApplication
import sys

class single_chat(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 800)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 50, 200, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(50, 100, 700, 500))
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(50, 620, 500, 60))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(600, 620, 150, 60))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 700, 700, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.retranslateUi()
        self.represented_name = ''
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Chatting With "))
        self.pushButton.setText(_translate("Dialog", "Send"))
        self.pushButton_2.setText(_translate("Dialog", "Close"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = single_chat()
    window.show()
    sys.exit(app.exec_())