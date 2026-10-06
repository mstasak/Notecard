# Event handling, UI updates, and biz logic for MainWindow.
# for separation of concerns, this knows nothing about MainWindow;

# Operations on view use eventcentral events and callbacks.

from datastructures import MsgRec, MsgArgRec
from messagehub import gMessageHub #, EventCentral
from typing import Any
import cardmodel
#import settings

#from datastructures import IdTitleRec

class MainController:
    def __init__(self) -> None:
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='cardSelectionChanged',
                           rspCall=self.recvCardSelChg)
        
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='cardDataSubmit',
                           rspCall=self.recvCardData)
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='srchDataSubmit',
                           rspCall=self.recvSrchData)

        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='newClicked',
                           rspCall=self.bnNewClicked)
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='saveClicked',
                           rspCall=self.bnSaveClicked)
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='deleteClicked',
                           rspCall=self.bnDeleteClicked)
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='searchClicked',
                           rspCall=self.bnSearchClicked)
        gMessageHub.listen(lsnrName='MainWindowController',
                           evtTopic='MainWindow(input)',
                           evtName='pickCatgClicked',
                           rspCall=self.bnPickCatgClicked)

        self.fillNotecardList()

    def bnNewClicked(self, sender: Any, evt: MsgRec):
        #if self.saveCardIfNeeded():
            #print('New clicked')
        pass

    def bnSaveClicked(self, sender: Any, evt: MsgRec):
        #if self.saveCardIfNeeded():
            #print('New clicked')
        if cardmodel.CardRecsEqual(evt.msgArgs[0].value,
                                   evt.msgArgs[1].value):
            self.sendStatus("No changes to save!")
        else:
            self.sendStatus("saved.")
            c = cardmodel.Notecard()
            c.loadNotecardRec(evt.msgArgs[1].value)
            c.save(cardmodel.gModel)
        #print(evt)

    def sendStatus(self, s: str) -> None:
        gMessageHub.post(sender='MainWindowController',
                         event=MsgRec(
                             topic='MainWindow(output)',
                             msgName='fillStatus',
                             msgArgs=[
                                 MsgArgRec(name='newMessage', value=s),
                             ]))

    def bnDeleteClicked(self, sender: Any, evt: MsgRec):
        print('Delete clicked', sender, evt)

    def bnSearchClicked(self, sender: Any, evt: MsgRec):
         print('Search clicked', sender, evt)

    def bnPickCatgClicked(self, sender: Any, evt: MsgRec):
        print('Pick categories clicked', sender, evt)

    def recvCardData(self, sender: str, evt: MsgRec):
        print('Card data received', sender, evt)

    def recvSrchData(self, sender: str, evt: MsgRec):
        print('Search data received', sender, evt)

    def fillSrchData(self, target: str):
        gMessageHub.post(sender='MainWindowController',
                         event=MsgRec(
                             topic='MainWindow(output)',
                             msgName='fillSrchData',
                             msgArgs=[
                                 MsgArgRec(name='srchString', value='target'),
                                 #MsgArgRec(name='', value=''),
                             ]))

    def fillCardData(self, card: cardmodel.Notecard) -> None:
        gMessageHub.post(sender='MainWindowController',
                         event=MsgRec(
                             topic='MainWindow(output)',
                             msgName='fillCardData',
                             msgArgs=[
                                 MsgArgRec(name='rowData',
                                           value=card.toCardRec()),
                                 #MsgArgRec(name='', value=''),
                             ]))

    def fillNotecardList(self) -> None:
        #query id, titles
        #post list to view
        cardList = cardmodel.CardList()
        cardList.load(cardmodel.gModel)
        #print(cardList.cardTitles)
        gMessageHub.post(sender='MainWindowController',
                         event=MsgRec(
                             topic='MainWindow(output)',
                             msgName='fillCardListData',
                             msgArgs=[
                                 MsgArgRec(name='CardIdTitlesData',
                                           value=cardList.cardTitles),
                             ]))

    def recvCardSelChg(self, sender: str, evt: MsgRec):
        #receive    self.ec.post(
        #               sender='MainWindow',
        #               event=EventRec(
        #                   topic='MainWindow(input)',
        #                   msgName='cardSelectionChanged',
        #                   msgArgs=[(EventArgRec(
        #                       name='newIndex',
        #                       value=self.listViewNotecards.currentIndex().row())
        #                   )]
        #               )
        #           )

        #print('Card selection changed', sender, evt)
        # 1. if old card exists and is modified, fetch from UI and save to db
        # 2. fetch new detail data from db and push to UI
        cardId: int = evt.msgArgs[1].value #selectedNotecardId'
        card = cardmodel.Notecard()
        card.loadWithId(model=cardmodel.gModel, notecardId=cardId)
        self.fillCardData(card)

    def shutdown(self) -> None:
        gMessageHub.removeListener(lsnrName='MainWindowController')
