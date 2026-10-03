# Event handling, UI updates, and biz logic for CFMainWindow.
# for separation of concerns, this knows nothing about CFMainWindow;

# Operations on view use eventcentral events and callbacks.

from datastructures import MsgRec, MsgArgRec
from messagehub import gMessageHub #, EventCentral
from typing import Any
import model
#from datastructures import IdTitleRec

class CFMainWindowController:
    def __init__(self) -> None:
        gMessageHub.listen(lsnrName='CFMainWindowController', evtTopic='CFMainWindow(input)',
                           evtName='cardSelectionChanged', rspCall=self.recvCardSelChg)
        
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='cardDataSubmit',rspCall=self.recvCardData)
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='srchDataSubmit',rspCall=self.recvSrchData)

        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='newClicked',rspCall=self.bnNewClicked)
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='saveClicked',rspCall=self.bnSaveClicked)
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='deleteClicked',rspCall=self.bnDeleteClicked)
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='searchClicked',rspCall=self.bnSearchClicked)
        gMessageHub.listen(lsnrName='CFMainWindowController',evtTopic='CFMainWindow(input)',
                           evtName='pickCatgClicked',rspCall=self.bnPickCatgClicked)

        self.fillNotecardList()

    def bnNewClicked(self, sender: Any, evt: MsgRec):
        #if self.saveCardIfNeeded():
            #print('New clicked')
        pass

    def bnSaveClicked(self, sender: Any, evt: MsgRec):
        #if self.saveCardIfNeeded():
            #print('New clicked')
        if model.CardRecsEqual(evt.eventargs[0].value, evt.eventargs[1].value):
            self.sendStatus("No changes to save!")
        else:
            self.sendStatus("Pretending to save...")
            c = model.Notecard()
            c.loadNotecardRec(evt.eventargs[1].value)
            c.save(model.gModel)
        #print(evt)

    def sendStatus(self, s: str) -> None:
        gMessageHub.post(sender='CFMainWindowController',
                         event=MsgRec(
                             topic='CFMainWindow(output)',
                             eventname='fillStatus',
                             eventargs=[
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
        gMessageHub.post(sender='CFMainWindowController',
                         event=MsgRec(topic='CFMainWindow(output)',
                                        eventname='fillSrchData',
                                        eventargs=[
                                            MsgArgRec(name='srchString', value='target'),
                                            #EventArgRec(name='', value=''),
                                        ]
                                       )
                         )

    def fillCardData(self, card: model.Notecard) -> None:
        gMessageHub.post(sender='CFMainWindowController',
                         event=MsgRec(
                             topic='CFMainWindow(output)',
                             eventname='fillCardData',
                             eventargs=[
                                 MsgArgRec(name='rowData', value=card.toCardRec()),
                                 #   EventArgRec(name='title', value=card.title),
                                 #   EventArgRec(name='body', value=card.body),
                                 #   EventArgRec(name='id', value=card.id),
                                 #   EventArgRec(name='catgs', value=card.categories),
                                 #   EventArgRec(name='selcatgids', value=[1,2]),
                                 #   EventArgRec(name='', value=''),
                                 #   EventArgRec(name='', value=''),
                              ]))

    def fillNotecardList(self) -> None:
        #query id, titles
        #post list to view
        cardList = model.CardList()
        cardList.load(model.gModel)
        #print(cardList.cardTitles)
        gMessageHub.post(sender='CFMainWindowController',
                         event=MsgRec(topic='CFMainWindow(output)',
                                        eventname='fillCardListData',
                                        eventargs=[
                                            MsgArgRec(name='CardIdTitlesData', value=cardList.cardTitles),
                                        ]
                                       )
                         )


    def recvCardSelChg(self, sender: str, evt: MsgRec):
        #receive    self.ec.post(
        #               sender='CFMainWindow',
        #               event=EventRec(
        #                   topic='CFMainWindow(input)',
        #                   eventname='cardSelectionChanged',
        #                   eventargs=[(EventArgRec(
        #                       name='newIndex',
        #                       value=self.listViewNotecards.currentIndex().row())
        #                   )]
        #               )
        #           )

        #print('Card selection changed', sender, evt)
        # 1. if old card exists and is modified, fetch from UI and save to db
        # 2. fetch new detail data from db and push to UI
        cardId: int = evt.eventargs[1].value #selectedNotecardId'
        card = model.Notecard()
        card.loadWithId(model=model.gModel, notecardId=cardId)
        self.fillCardData(card)

    def shutdown(self) -> None:
        gMessageHub.removeListener(lsnrName='CFMainWindowController')

