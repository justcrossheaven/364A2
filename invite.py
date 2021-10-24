from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QApplication
import sys


class invite(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(400, 800)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(50, 10, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(50, 50, 301, 621))
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(50, 700, 131, 51))
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 700, 121, 51))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Connected Clients"))
        self.pushButton.setText(_translate("Dialog", "Invite"))
        self.pushButton_2.setText(_translate("Dialog", "Cancel"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = invite()
    window.show()
    sys.exit(app.exec_())