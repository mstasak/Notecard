from typing import Any

from datastructures import MsgRec, ListenForRec #, EventArgRec, DelivererRec

class MessageCenter:

    def __init__(self) -> None:
        self._listeners: list[ListenForRec] = []

    def post(self, sender: str, event: MsgRec) -> None:
        lRec: ListenForRec
        for lRec in self._listeners:
            if ((lRec.topic == '*' or lRec.topic == event.topic) and
               (lRec.eventName == "*" or lRec.eventName == event.eventname)):
                #send it
                # e = EventRec('topic',
                #              'myevent',
                #              [EventArgRec(name='x',value=1),
                #               EventArgRec(name='y',value=2)])
                lRec.deliverer(sender, event)
            # comment: 
        # end for

    def listen(self, lsnrName: str, evtTopic: str, evtName: str, rspCall: Any) -> None:
        #pass
        #check if already listening
        #skip if matched; replace if more general?
        self._listeners.append(
            ListenForRec(
                listenerName=lsnrName,
                topic=evtTopic,
                eventName=evtName,
                #sender='any',
                deliverer=rspCall
            ))

    def removeListener(self, lsnrName: str) -> None:
        #element:ListenerRec
        #self._listeners.remove(element)
        self._listeners = list(filter(lambda x: x.listenerName != lsnrName, self._listeners))

    #def __del__(self) -> None:
        #GC would do this
        #self._listeners = {}

#global singleton (casual)
gMessageHub: MessageCenter = MessageCenter()

### GETTING MESSY, MIGHT WANT TO SIMPLIFY/RESTART

