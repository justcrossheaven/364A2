import os
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, QUrl, QEventLoop
from PyQt5.QtWidgets import *
from connect import connect_page
from try_client import ChatClient
from main import MainWindow
from groupchat import group_chat
from singlechat import single_chat
from invite import invite
from PyQt5.QtCore import pyqtSlot, pyqtSignal 

class App(QMainWindow):
    
    def __init__(self):
        super(App, self).__init__()
        self.connect = connect_page()
        self.connect.pushButton.clicked.connect(self.try_connect)
        # self.client.usr_signal.connect(self.showUsers)
        self.main = MainWindow()
        # self.singlechat = single_chat()
        # self.invite = invite()
        # self.groupchat = group_chat()
        self.main.listView.itemActivated.connect(self.selectSingleChat)
        self.main.listView_2.itemSelectionChanged.connect(self.selectGroupChat)
        self.main.pushButton.clicked.connect(self.startSingleChat)
        self.main.pushButton_2.clicked.connect(self.createGroupChat)
        self.main.pushButton_3.clicked.connect(self.joinGroupChat)
        self.main.pushButton_4.clicked.connect(self.closeEvent)
        quit = QAction("Quit", self.main)
        quit.triggered.connect(self.closeEvent)
        self.list_single_user = [[], []] # 0 for name to, 1 for single_chat
        self.list_groups = [] # list of users list that the user is in  [["a", "b","c"],["a", "b"], ["b", "c"]]
        self.group_windows = [[], []] # list of windows that u are in [[1, 3, 4, 5], [window, window]]

    def try_connect(self):
        ipaddress = self.connect.textEdit.toPlainText()
        port = int(self.connect.textEdit_2.toPlainText())
        name = self.connect.textEdit_3.toPlainText()
        self.client = ChatClient(ipaddress, port)
        self.client.usr_signal.connect(self.updateUserList)
        self.client.text_signal.connect(self.showText)
        self.client.connect()
        self.client.start()
        self.name = name
        self.main.show()
        self.connect.close()
        self.client.addData("NEW_USR", '', name)

    def updateUserList(self, user_list):
        print(user_list)
        users = user_list['users']
        self.all_user_list = users
        groups = user_list['groupsall']
        self.list_groups = user_list['group_mem']
        items = []
        i_groups = []
        self.main.listView.clear()
        self.main.listView_2.clear()
        for i in range(self.main.listView.count()):
            items.append(self.main.listView.item(i).text())
        for j in range(self.main.listView_2.count()):
            i_groups.append(self.main.listView_2.item(j).text())
        for user in users:
            if user != self.name:
                self.main.listView.addItem(user)
        for group in groups:
            self.main.listView_2.addItem(str(group))
        for group_window in self.group_windows[1]:
            group_window.listView.clear()
            for m in self.list_groups[self.group_windows[1].index(group_window)]:
                group_window.listView.addItem(m)
        
    
    def selectSingleChat(self):
        print("Selected items: ", self.main.listView.selectedItems())
        for item in self.main.listView.selectedItems():
            self.selected_user = item.text()
        self.main.pushButton.setDisabled(False)

        
    def selectGroupChat(self):
        print("Selected items: ", self.main.listView_2.selectedItems())
        for item in self.main.listView_2.selectedItems():
            self.selected_group = item.text()
        self.main.pushButton_3.setDisabled(False)
    
    def createGroupChat(self):
        self.list_groups.append([self.name])
        index = len(self.list_groups) - 1
        data = {'ind': index, 'name': self.name}
        self.client.addData('JOIN', 'CREATE', data)
        self.group_windows[0].append(index)
        curr_group_chat = group_chat()
        curr_group_chat.pushButton.clicked.connect(lambda: self.g_sendmsg(curr_group_chat))
        curr_group_chat.pushButton_2.clicked.connect(lambda: self.invite(curr_group_chat))
        self.group_windows[1].append(curr_group_chat)
        curr_group_chat.show()


    def joinGroupChat(self):
        index = int(self.selected_group)
        self.group_windows[0].append(index)
        self.list_groups[index].append(self.name)
        data = {'ind':index, 'name': self.name}
        self.client.addData('JOIN', 'JOIN', data)
        curr_group_chat = group_chat()
        curr_group_chat.pushButton.clicked.connect(lambda: self.g_sendmsg(curr_group_chat))
        curr_group_chat.pushButton_2.clicked.connect(lambda: self.invite(curr_group_chat))
        self.group_windows[1].append(curr_group_chat)
        curr_group_chat.show()


    def startSingleChat(self):
        self.list_single_user[0].append(self.selected_user)
        current_single = single_chat()
        current_single.pushButton.clicked.connect(lambda: self.sendmsg(current_single))
        current_single.represented_name = self.selected_user
        current_single.show()
        self.list_single_user[1].append(current_single)

    
    def showText(self, text):
        text_from = text['msg_from']
        if isinstance(text_from, str):
            if text_from in self.list_single_user[0]:
                i = self.list_single_user[0].index(text_from) 
                self.list_single_user[1][i].listView.addItem(text_from + ":  " + text['msg'])
            else:
                self.list_single_user[0].append(text_from)
                current_single = single_chat()
                current_single.pushButton.clicked.connect(lambda: self.sendmsg(current_single))
                current_single.represented_name = text_from
                current_single.show()
                current_single.listView.addItem(text_from + ":  " + text['msg'])
                self.list_single_user[1].append(current_single)
        elif isinstance(text_from, int):
            user = text['user']
            msg = text['msg']
            if text_from in self.group_windows[0] and user != self.name:
                index = self.group_windows[0].index(text_from)
                self.group_windows[1][index].listView_2.addItem(user + ":  " + msg)
        print(text)
    
    def sendmsg(self, single):
        to = single.represented_name
        text = single.textEdit.toPlainText()
        single.listView.addItem(self.name + " (You):  " + text)
        data = {'msg_to': to, 'msg': text}
        self.client.addData('MSG', '', data)
        single.textEdit.clear()
    
    def g_sendmsg(self, group):
        to = group.represented_name
        text = group.textEdit.toPlainText()
        group.listView_2.addItem(self.name + " (You):  " + text)
        data = {'msg_to': to, 'msg': text}
        self.client.addData('MSG', '', data)
        group.textEdit.clear()

    
    def invite(self, group):
        index = group.represented_name
        user_list = self.list_groups[index]
        invitable_user = list(set(self.all_user_list) - set(user_list))
        
        for m in invitable_user:
            group.invite.listView.addItem(m)
        group.invite.pushButton.clicked.connect(lambda: self.send_invite(group))
        group.invite.show()
    
    def send_invite(self, group):
        index = group.represented_name
        for item in group.invite.listView.selectedItems():
            name = item.text()
        data = {'ind': index, 'name': name}
        self.client.addData('JOIN', 'JOIN', data)
        group.invite.close()
    
    def closeEvent(self, event):
        self.close = QMessageBox()
        self.close.setText("You sure?")
        self.close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        self.close = close.exec()
        if self.main.close == QMessageBox.Yes:
            self.connect.show()
            self.client.sock.shutdown()
            event.accept()
        else:
            event.ignore()

    
    
    
    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # connect_page = App()
    # connect_page.show()
    App = App()
    App.connect.show()
    sys.exit(app.exec_())