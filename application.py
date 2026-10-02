# NOTECARDS APP
# Windows 11, Python 3.14.6+, PySide 6.1+, SQLite 3+
# using a shared .venv; may need to use PS G:\Dev\Python\ExperimentZone> ..\.shared_venv\scripts\activate.ps1 

#import sys
#import logging
from PySide6 import QtWidgets #, QtCore, QtGui
from PySide6.QtWidgets import QMainWindow
#from PySide6.QtCore import QSettings #, QCoreApplication
import model
from cfMainWindow import CFMainWindow
from cfMainWindowController import CFMainWindowController
from model import CardfileModel
from typing import Any
#from settings import gSettings
#import services

# APP
class CardFileApp(QtWidgets.QApplication):

    #global app #: CardFileApp
    #settings: QSettings
    #model: model.CardfileModel
    #services.gLogger = logging.getLogger()
    #services.gLogger.info("logger opened at stream?")

    def __init__(self, orgName:str, orgDomain:str, appName:str, args: list[Any]) -> None:
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
        
        #services.gSettings.setValue("prevwhatsit", self.settings.value("whatsit"))
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

# Settings

# Search

# Keyword Manager

# keyword selection

#main

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