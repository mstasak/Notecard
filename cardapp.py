# NOTECARDS APP
# Windows 11, Python 3.14.6+, PySide 6.1+, SQLite 3+
# using a shared .venv; may need to use
# PS G:\Dev\Python\Notecard> ..\.shared_venv\scripts\activate.ps1 

# System imports
from typing import Any
#import sys
#import logging

# 3rd party lib imports
from PySide6 import QtWidgets #, QtCore, QtGui
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QSettings, QSize #, QCoreApplication
#from PySide6.QtCore import (Qt, QCoreApplication, QMetaObject, QObject, QRect)
#QDate, QDateTime, QLocale, QPoint, QTime, QUrl

# internal app imports
import cardmodel
from cardmodel import CardModel
from mainview import MainView
from maincontroller import MainController
import settings
#import services

# QT Application class, instantiated by Notecards.py.
class CardApp(QtWidgets.QApplication):

    def __init__(self, orgName:str, orgDomain:str, appName:str, 
                 args: list[Any]) -> None:
        super().__init__(args)
        #self.window: QMainWindow
        #self.windowController: MainWindowController
        #global gApp
        self.setOrganizationName(orgName)
        self.setOrganizationDomain(orgDomain)
        self.setApplicationName(appName)
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        global gSettings
        self.settings = QSettings()
        
        settings.gSettings = self.settings
        settings.startup()
        #self.settings.sync() #needed? no
        
        #services.gSettings.setValue("prevwhatsit",
        #                            self.settings.value("whatsit"))
        #services.gSettings.setValue("whatsit", "test1")
        #self.model = model.CardfileModel()

    def run(self) -> int:
        window = MainWindow()
        cardmodel.gModel = CardModel()
        #window.windowContent = MainWindowView()
        windowController = MainController()
        #window.setGeometry(100, 100, 1000, 700)
        #windowContent:Ui_MainWindow
        #widget = MyWidget()
        #widget.resize(800, 600)
        #widget.show()
        window.show()
        
        rslt = self.exec()
        windowController.shutdown()
        if settings.ScreenRememberPosSize:
            settings.ScreenSize = window.size()
            settings.ScreenPos = window.pos()
        settings.shutdown()
        return rslt

# This is the top window object created by CardFileApp.
# All it does is hold a MainView container widget.
# Seems useless, but eliminating it or using QMainWindow
# instead of a subclass seemed to cause problems. 
class MainWindow(QMainWindow):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        #self.setWindowTitle('Editor')
        #self.setWindowIcon(QIcon('./assets/editor.png'))
        #self.setGeometry(100, 100, 500, 300)
        #settings.startup()
        self.setMinimumSize(QSize(640, 480))
        self.move(settings.ScreenPos)
        self.resize(settings.ScreenSize)

        self.windowContent = MainView()
        self.windowContent.setupUi(self)

    # closeEvent(self, event): #BUGGY?  MyPy complains unknown event - maybe
    #                          #works on QWidget but not QMainWindow?
    #     settings.gSettings.setValue("pos", self.pos)
    #     settings.gSettings.setValue("size", self.size)
    #     super.closeEvent(event)
    #     event.accept()

if __name__ == "__main__":
    pass