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
#from PySide6.QtCore import QSettings #, QCoreApplication

# internal app imports
import model
from model import CardfileModel
from cfMainWindow import CFMainWindow
from cfMainWindowController import CFMainWindowController
#from settings import gSettings
#import services

# QT Application class, instantiated by Notecards.py.
class CardFileApp(QtWidgets.QApplication):

    def __init__(self, orgName:str, orgDomain:str, appName:str, 
                 args: list[Any]) -> None:
        super().__init__(args)
        #self.window: QMainWindow
        #self.windowController: CFMainWindowController
        #global gApp
        self.setOrganizationName(orgName)
        self.setOrganizationDomain(orgDomain)
        self.setApplicationName(appName)
        #QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        #self.settings = QSettings()
        #services.gSettings = self.settings
        #self.settings.sync() #needed? no
        
        #services.gSettings.setValue("prevwhatsit",
        #                            self.settings.value("whatsit"))
        #services.gSettings.setValue("whatsit", "test1")
        #self.model = model.CardfileModel()

    def run(self) -> int:
        window = MainWindow()
        model.gModel = CardfileModel()
        window.windowContent = CFMainWindow()
        windowController = CFMainWindowController()
        #window.setGeometry(100, 100, 1000, 700)
        window.show()
        #windowContent:Ui_MainWindow
        #widget = MyWidget()
        #widget.resize(800, 600)
        #widget.show()
        rslt =self.exec()
        windowController.shutdown()
        return rslt

# This is the top window object created by CardFileApp.
# All it does is hold a CFMainWindow container widget.
# Seems useless, but eliminating it or using QMainWindow
# instead of a subclass seemed to cause problems. 
class MainWindow(QMainWindow):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        #self.setWindowTitle('Editor')
        #self.setWindowIcon(QIcon('./assets/editor.png'))
        #self.setGeometry(100, 100, 500, 300)
        self.windowContent = CFMainWindow()
        self.windowContent.setupUi(self)

if __name__ == "__main__":
    pass