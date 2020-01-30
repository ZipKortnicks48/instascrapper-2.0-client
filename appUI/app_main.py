
import formsUI.form_main as form_main
from appUI.app_server_settings import AppServerSettings
from src.formHandler import formHandler
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QSystemTrayIcon,QStyle,QAction,qApp,QMenu
from datetime import datetime
from threading import Thread
import schedule
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
class App(QtWidgets.QMainWindow, QtWidgets.QTableWidgetItem, form_main.Ui_Dialog,QtWidgets.QErrorMessage,QtWidgets.QHeaderView):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.startEvent = True
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.showCommentsButton.pressed.connect(self.showCommentsButtonClick)
        self.buttonHand.pressed.connect(self.handSearch)
        # #иконка трея
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
 
        # '''
        #     show - показать окно
        #     hide - скрыть окно
        #     exit - выход из программы
        # '''
        # show_action = QAction("Развернуть", self)
        # quit_action = QAction("Выход", self)
        # hide_action = QAction("Скрыть", self)
        # show_action.triggered.connect(self.show)
        # hide_action.triggered.connect(self.hide)
        # quit_action.triggered.connect(qApp.quit)
        # tray_menu = QMenu()
        # tray_menu.addAction(show_action)
        # tray_menu.addAction(hide_action)
        # tray_menu.addAction(quit_action)
        # self.tray_icon.setContextMenu(tray_menu)
        # self.tray_icon.show()
        # self.newServerSettingsItem.triggered.connect(self.showNewServerSettingsWindow)
    def showNewServerSettingsWindow(self):
        self.windowServer = AppServerSettings()  # Создаём объект класса ExampleApp
        self.windowServer.show()  # Показываем окно
    #ручной поиск по словам 
    def handSearch(self):
        word=self.textBoxSearch.text()
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        self.tableComments.clear()
        comments=self.handler.bdAPI.getCommentHandsearch(word)
        self.tableComments.setRowCount(len(comments))
        row=0
        for comment in comments:
                self.tableComments.setItem(row, 0,  QtWidgets.QTableWidgetItem(datetime.fromtimestamp(int(comment["comment_date"])).strftime("%d-%m-%Y %H:%M")))
                self.tableComments.setItem(row, 1,  QtWidgets.QTableWidgetItem(comment["comment_text"]))
                self.tableComments.setItem(row, 2,  QtWidgets.QTableWidgetItem(self.handler.bdAPI.getLinkByCommentId(comment["comment_id"])))
                row += 1
        self.setHeaderTittle()
        QMessageBox.about(self,"Уведомление","Поиск завершен")
    def enableButtons(self):
        self.autoButton.setEnabled(True)
        self.findNewComButton.setEnabled(True)
    #отобразить найденные комменты по словарю
    def showCommentsButtonClick(self):
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        self.tableComments.clear()
        comments=self.handler.bdAPI.showGoodComments()
        self.tableComments.setRowCount(len(comments))
        row=0
        for comment in comments:
                self.tableComments.setItem(row, 0,  QtWidgets.QTableWidgetItem(datetime.fromtimestamp(int(comment['comment_date'])).strftime("%d-%m-%Y %H:%M")))
                self.tableComments.setItem(row, 1,  QtWidgets.QTableWidgetItem(comment['comment_text']))
                self.tableComments.setItem(row, 2,  QtWidgets.QTableWidgetItem(self.handler.bdAPI.getLinkByCommentId(comment['comment_id'])))
                row += 1
        self.setHeaderTittle()
        QMessageBox.about(self,"Уведомление","Поиск завершен")
    #поиск по новому словарю
    def searchButtonClick(self):
        username=self.comboBoxAcc.currentText()
        self.handler=formHandler(username)
        #QMessageBox.about(self,"Уведомление","Ищем по новому словарю") 
        self.handler.bdAPI.checkComments()
    #событие закрытия окна
    # def closeEvent(self, event):
    #     event.ignore()
    #     self.hide()
    #     self.tray_icon.showMessage(
    #         "Программа свернута",
    #         "Программа была свернута в трей.",
    #         QSystemTrayIcon.Information,
    #         2000
    #         )
    def setHeaderTittle(self):
        self.tableComments.setHorizontalHeaderLabels(['Дата', 'Текст', 'Ссылка на запись'])