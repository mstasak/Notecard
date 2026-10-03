# -*- coding: utf-8 -*-

# Main view (edit form) for notecard app, with menu
# serviced by a controller via messages & listeners.
# Controller and view have no internal knowledge of 
# each other's implementation, like class, function,
# or variable names.

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# system imports
from copy import deepcopy
from typing import Any

# QT(PySide6) imports
from PySide6.QtCore import (Qt, QCoreApplication, QMetaObject, QObject, QRect)
#QDate, QDateTime, QLocale, QPoint, QSize, QTime, QUrl

from PySide6.QtGui import (QAction #, QBrush, QColor, QConicalGradient,
    #QCursor, QFont, QFontDatabase, QGradient,
    #QIcon, QImage, QKeySequence, QLinearGradient,
    #QPainter, QPalette, QPixmap, QRadialGradient,
    #QTransform
    )

from PySide6.QtWidgets import ( #QApplication,
    QGroupBox, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, #QCheckBox, QSizePolicy,
    QStatusBar, QTextEdit, QWidget)

#from PySide6.QtCore.Qt import QAlignment

#project-local imports
from messagehub import gMessageHub #, MessageCenter
from datastructures import (CardRec, CategoryRec, CardIdTitleRec,
    MsgRec, MsgArgRec)

class CFMainWindow(QObject):

    def __init__(self) -> None:
        super().__init__()
        self.msgHub = gMessageHub
        self.origCardData = CardRec(
            notecardId=None,
            title='',
            body='',
            categories=[]
        )
    
    def saveCardDetails(self) -> None:
        pass

    def populateCardDetails(self, sender: str, evt: MsgRec) -> None: # type: ignore
        #print(sender)
        cRec: CardRec = evt.eventargs[0].value
        self.origCardData = deepcopy(cRec)
        #print(cRec)
        self.lineEditNotecardTitle.setText(cRec.title)
        self.textEditNotecardBody.setText(cRec.body)
        self.listWidgetCategories.clear()
        i = 0
        for cat in cRec.categories:
            self.listWidgetCategories.addItem(cat.title)
            item: QListWidgetItem = self.listWidgetCategories.item(i)
            #item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable) # is default
            item.setCheckState(Qt.CheckState.Checked if cat.selected else Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, cat.categoryId)
            i += 1

    def populateCardList(self, sender: str, evt: MsgRec) -> None: # type: ignore
        clRec: list[CardIdTitleRec] = evt.eventargs[0].value
        self.listViewNotecards.clear()
        i : int = 0
        for cat in clRec:
            self.listViewNotecards.addItem(cat.title)
            item: QListWidgetItem = self.listViewNotecards.item(i)
            item.setData(Qt.ItemDataRole.UserRole,cat.notecardId)
            i += 1

    def setupUi(self, MainWindow: QMainWindow):

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        #MainWindow.resize(924, 696)

        # region actions        
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionSearch = QAction(MainWindow)
        self.actionSearch.setObjectName(u"actionSearch")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        # endregion

        # region menu bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 924, 33))
        self.menuNotecard = QMenu(self.menubar)
        self.menuNotecard.setObjectName(u"menuNotecard")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuNotecard.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuNotecard.addAction(self.actionNew)
        self.menuNotecard.addAction(self.actionSearch)
        self.menuNotecard.addAction(self.actionDelete)
        self.menuNotecard.addSeparator()
        self.menuNotecard.addAction(self.actionExit)
        # endregion

        # region widget and layout hierarchies
        self.vBoxCentral = QWidget(MainWindow)
        self.vBoxCentral.setObjectName(u"centralWidget")
        self.vBoxCentralLayout = QVBoxLayout(self.vBoxCentral)
        self.vBoxCentralLayout.setObjectName(u"centralLayout")
        MainWindow.setCentralWidget(self.vBoxCentral)
        self.searchBar = QWidget(self.vBoxCentral)


        self.hBoxSearch = QWidget(self.vBoxCentral)
        self.hBoxSearchLayout = QHBoxLayout(self.hBoxSearch)

        self.hBoxListDetail = QWidget(self.vBoxCentral)
        self.hBoxListDetailLayout = QHBoxLayout(self.hBoxListDetail)
        self.vBoxCentralLayout.addWidget(self.hBoxSearch)
        self.vBoxCentralLayout.addWidget(self.hBoxListDetail)

        self.detailCmdWidget = QWidget(self.hBoxListDetail)
        self.detailCmdLayout = QVBoxLayout(self.detailCmdWidget)
        # endregion

        # region search bar
        self.labelSearch = QLabel(self.hBoxSearch)
        self.labelSearch.setObjectName(u"label")
        #self.labelSearch.setGeometry(QRect(30, 20, 49, 16))
        self.lineEditSearchText = QLineEdit(self.hBoxSearch)
        self.lineEditSearchText.setObjectName(u"lineEdit")
        #self.lineEditSearchText.setGeometry(QRect(80, 20, 711, 26))
        self.pushButtonSearch = QPushButton(self.hBoxSearch)
        self.pushButtonSearch.setObjectName(u"pushButton")
        #self.pushButtonSearch.setGeometry(QRect(800, 20, 81, 26))
        
        self.hBoxSearchLayout.addWidget(self.labelSearch)
        self.hBoxSearchLayout.addWidget(self.lineEditSearchText)
        self.hBoxSearchLayout.addWidget(self.pushButtonSearch)
        # endregion

        # region notecard list
        self.listViewNotecards = QListWidget(self.hBoxListDetail)
        self.listViewNotecards.setObjectName(u"listView")
        #self.listViewNotecards.setGeometry(QRect(30, 60, 851, 241))
        self.hBoxListDetailLayout.addWidget(self.listViewNotecards)
        #self.listViewNotecards.addItems(["card1","card2","card 99"])
        #self.listViewNotecards.itemSelectionChanged.connect(self.lvcChanged)
        self.listViewNotecards.itemSelectionChanged.connect(
            lambda:
                self.msgHub.post(
                    sender='CFMainWindow',
                    event=MsgRec(
                        topic='CFMainWindow(input)',
                        eventname='cardSelectionChanged',
                        eventargs=[
                            MsgArgRec(
                                name='selectedRow',
                                value=self.listViewNotecards.currentIndex().row()
                            ),
                            MsgArgRec(
                                name='selectedNotecardId',
                                value=self.listViewNotecards.item(
                                    self.listViewNotecards.currentIndex().row())
                                    .data(Qt.ItemDataRole.UserRole)
                            ),
                        ]
                    )
                )
        )
        # endregion

        # region notecard details
        # all in 2nd cell of hBoxListDetail (above)
        #self.hBoxListDetail = QWidget(self.vBoxCentral)
        #self.hBoxListDetailLayout = QHBoxLayout(self.hBoxListDetail)

        self.buildDetailSection()
        # endregion

        #status bar
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.labelStatus = QLabel(text="")
        #self.labelStatus.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        #self.labelStatus.setMargin(5)
        #self.labelStatus.setIndent(10)
        #self.labelStatus.setAlignment(AlignmentFlag.Center)
        self.labelStatus.setObjectName(u"labelStatus")
        #self.statusbar.addWidget()
        self.statusbar.addWidget(self.labelStatus)
        MainWindow.setStatusBar(self.statusbar)

        #self.centralVBox = QVBoxLayout(self.centralwidget)
        #self.centralVBox.setObjectName(u"centralvbox")


        self.retranslateUi(MainWindow) #needed even for one lang - sets UI text literals for default language
        QMetaObject.connectSlotsByName(MainWindow)
        self.msgHub.listen(
            lsnrName='CFMainWindow',
            evtTopic='CFMainWindow(output)',
            evtName='fillCardData',
            rspCall=self.populateCardDetails
        )
        self.msgHub.listen(
            lsnrName='CFMainWindow',
            evtTopic='CFMainWindow(output)',
            evtName='fillCardListData',
            rspCall=self.populateCardList
        )
        self.msgHub.listen(
            lsnrName='CFMainWindow',
            evtTopic='CFMainWindow(output)',
            evtName='fillStatus',
            rspCall=self.changeStatus
        )

    def changeStatus(self, sender: str, evt: MsgRec) -> None:
        self.labelStatus.setText(evt.eventargs[0].value)

    # setupUi

    # def lvcChanged(self):
    #     #documentation is horrible, keep this expression returning current row
    #     #works well for single-selection mode, although it returns current row if it is 
    #     #deselected (e.g. with ctrl+space)
    #     print("Row: ", self.listViewNotecards.currentIndex().row())

    def buildDetailSection(self):
        # , Parent:QWidget, HBox:QHBoxLayout
        self.vBoxDetailCommand = QWidget(self.hBoxListDetail)
        self.vBoxDetailCommandLayout = QVBoxLayout(self.vBoxDetailCommand) #QGroupBox
        self.hBoxListDetailLayout.addWidget(self.vBoxDetailCommand)
        self.groupDetail = QGroupBox(self.vBoxDetailCommand)

        self.groupDetail.setObjectName(u"groupDetail")
        self.groupDetailLayout = QHBoxLayout()
        self.groupDetail.setLayout(self.groupDetailLayout)

        self.detailGrid = QWidget(self.groupDetail)
        self.detailGridLayout = QGridLayout(self.detailGrid)

        self.vBoxCatgEdit = QWidget(self.groupDetail)
        self.vBoxCatgEditLayout = QVBoxLayout(self.vBoxCatgEdit)

        self.groupDetailLayout.addWidget(self.detailGrid)
        self.groupDetailLayout.addWidget(self.vBoxCatgEdit)


        #self.groupDetail.setGeometry(QRect(30, 310, 851, 281))
        self.lineEditNotecardTitle = QLineEdit(self.groupDetail)
        self.lineEditNotecardTitle.setObjectName(u"lineEditNotecardTitle")
        #self.lineEditNotecardTitle.setGeometry(QRect(20, 30, 811, 26))
        self.textEditNotecardBody = QTextEdit(self.groupDetail)
        self.textEditNotecardBody.setObjectName(u"textEditNotecardBody")
        #self.textEditNotecardBody.setGeometry(QRect(20, 70, 601, 191))
        self.labelTitle = QLabel(self.groupDetail, text="Title")
        self.labelBody = QLabel(self.groupDetail, text="Description")
        
        self.labelCategories = QLabel(self.vBoxCatgEdit)
        self.labelCategories.setObjectName(u"labelCategories")
        #self.labelCategories.setGeometry(QRect(660, 70, 61, 16))
        self.listWidgetCategories = QListWidget(self.vBoxCatgEdit)
        self.listWidgetCategories.setObjectName(u"listWidgetCategories")
        #self.listWidgetCategories.setGeometry(QRect(660, 90, 161, 141))
        self.pushButtonEditCategories = QPushButton(self.vBoxCatgEdit)
        self.pushButtonEditCategories.setObjectName(u"pushButtonEditCategories")
        #self.pushButtonEditCategories.setGeometry(QRect(740, 240, 81, 26))
        self.vBoxCatgEditLayout.addWidget(self.labelCategories)
        self.vBoxCatgEditLayout.addWidget(self.listWidgetCategories)
        self.vBoxCatgEditLayout.addWidget(self.pushButtonEditCategories)
        
        self.detailGridLayout.addWidget(self.labelTitle,0,0)
        self.detailGridLayout.addWidget(self.labelBody,1,0,alignment=Qt.AlignmentFlag.AlignTop)
        self.detailGridLayout.addWidget(self.lineEditNotecardTitle,0,1)
        self.detailGridLayout.addWidget(self.textEditNotecardBody,1,1)
        self.lineEditNotecardTitle.setPlaceholderText("(title of notecard)")
        self.textEditNotecardBody.setPlaceholderText("(text of notecard)")
        

        # region edit commands (below details)
        self.hBoxEditCommands = QWidget(self.groupDetail) #just to center the button group?
        self.hBoxEditCommands.setObjectName(u"hBoxEditCommands")
        #self.hBoxEditCommands.setGeometry(QRect(180, 600, 511, 41))

        self.hBoxEditCommandLayout = QHBoxLayout(self.hBoxEditCommands) #contains edit command buttons
        self.hBoxEditCommandLayout.setObjectName(u"hLayoutEditCommands")
        self.hBoxEditCommandLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButtonNew = QPushButton(self.hBoxEditCommands)
        self.pushButtonNew.setObjectName(u"pushButtonNew")
        self.hBoxEditCommandLayout.addWidget(self.pushButtonNew)

        self.pushButtonSave = QPushButton(self.hBoxEditCommands)
        self.pushButtonSave.setObjectName(u"pushButtonSave")
        self.hBoxEditCommandLayout.addWidget(self.pushButtonSave)

        self.pushButtonDelete = QPushButton(self.hBoxEditCommands)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")
        self.hBoxEditCommandLayout.addWidget(self.pushButtonDelete)

        # self.pushButtonNew.clicked.connect(self.newClicked)
        self.pushButtonNew.clicked.connect(
            lambda: self.msgHub.post(sender='CFMainWindow',
                                 event=MsgRec(
                                     topic='CFMainWindow(input)',
                                     eventname='newClicked',
                                     eventargs=[])))
        self.pushButtonSave.clicked.connect(
            self.saveClicked
            # lambda: self.ec.post(sender='CFMainWindow',
            #                      event=EventRec(
            #                          topic='CFMainWindow(input)',
            #                          eventname='saveClicked',
            #                          eventargs=[]
            #                      )
            # )
        )
        self.pushButtonDelete.clicked.connect(
            lambda: self.msgHub.post(sender='CFMainWindow', 
                                 event=MsgRec(
                                     topic='CFMainWindow(input)',
                                     eventname='deleteClicked',
                                     eventargs=[])))

        self.vBoxDetailCommandLayout.addWidget(self.groupDetail)
        self.vBoxDetailCommandLayout.addWidget(self.hBoxEditCommands)

    # def newClicked(self):
    #     self.textEditNotecardBody.setText("New clicked")
    #     evt = EventRec(topic='CFMainWindow(input)',eventname='newClicked',eventargs=[])
    #     self.ec.post(sender='CFMainWindow', event=evt)

    def saveClicked(self):
        self.msgHub.post(sender='CFMainWindow',
                     event=MsgRec(
                         topic='CFMainWindow(input)',
                         eventname='saveClicked',
                         eventargs=[
                            MsgArgRec(
                                name='origRow',
                                value=self.origCardData # :CardRec
                            ),
                            MsgArgRec(
                                name='changedRow',
                                value=self.currentCardData() # :CardRec
                            ),
                         ]
                    )
        )

    def currentCardData(self) -> CardRec:
        return CardRec(
            notecardId=self.origCardData.notecardId,
            title=self.lineEditNotecardTitle.text(),
            body=self.textEditNotecardBody.toPlainText(),
            categories=self.categoryData()
        )


    def categoryData(self) -> list[CategoryRec]:
        #omitting title and description, and unchecked rows for efficiency
        #(all the controller really needs is a list of checked category ids)
        #code assumes category list is fixed - no additions, deletions, or reordering

        #safely convert Any to int
        def toInt(x:Any) -> int:
            return x if type(x) is int else 0

        #loop approach - maybe better
        #rslt: list[CategoryRec] = []
        #for i in range(self.listWidgetCategories.count()):
        #    print(i)
        #print('#catgs = ',self.listWidgetCategories.count())
        return [CategoryRec(
            #categoryId=self.origCardData.categories[i].categoryId,
            categoryId=toInt(self.listWidgetCategories.item(i).data(Qt.ItemDataRole.UserRole)), 
            title='', #self.origCardData.categories[i].title,
            description='', #self.origCardData.categories[i].description,
            selected=True #self.listWidgetCategories.item(i).checkState() == Qt.CheckState.Checked
          )
          for i in range(self.listWidgetCategories.count()) 
              if self.listWidgetCategories.item(i).checkState() == Qt.CheckState.Checked]
        #return rslt

    # def deleteClicked(self):
    #     self.textEditNotecardBody.setText("Delete clicked")

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Note Cards", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.labelSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.pushButtonSearch.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.groupDetail.setTitle(QCoreApplication.translate("MainWindow", u"Card Details", None))
        self.labelCategories.setText(QCoreApplication.translate("MainWindow", u"Categories", None))
        self.pushButtonEditCategories.setText(QCoreApplication.translate("MainWindow", u"Choose", None))
        self.pushButtonNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButtonSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.menuNotecard.setTitle(QCoreApplication.translate("MainWindow", u"Card", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi
