
from typing import cast
from PySide6.QtCore import QSettings, QPoint, QSize #, QCoreApplication

gSettings: QSettings
ScreenPos: QPoint
ScreenSize: QSize
ScreenRememberPosSize: bool

#App persistent settings,  Can't see any benefit to using a class singleton.

def startup():
    #Restore main window size and position, default if unknown or restore
    #disabled
    print(gSettings.fileName())
    global ScreenRememberPosSize
    ScreenRememberPosSize = cast(
        bool, 
        gSettings.value(
            "RememberAppWindowPos",
            defaultValue=True))
    global ScreenPos
    ScreenPos = cast(
        QPoint, 
        gSettings.value(
            "ScreenPos",
            defaultValue=QPoint(50,50)))
    global ScreenSize
    ScreenSize = cast(
        QSize,
        gSettings.value(
            "ScreenSize",
            defaultValue=QSize(640,480)))
    pass

def shutdown():
    #Save main window size and position
    global ScreenRememberPosSize
    gSettings.setValue("RememberAppWindowPos", ScreenRememberPosSize)
    global ScreenPos
    gSettings.setValue("ScreenPos", ScreenPos)
    global ScreenSize
    gSettings.setValue("ScreenSize", ScreenSize)
