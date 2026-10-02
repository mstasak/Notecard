from typing import NamedTuple, Any
from collections.abc import Callable

EventArgRec = NamedTuple('EventArgRec',[('name', str),('value', Any)])

EventRec = NamedTuple('EventRec', [('topic',str),('eventname',str),('eventargs', list[EventArgRec])])

DelivererRec = Callable[[str, EventRec],Any]   

ListenForRec = NamedTuple('ListenForRec',
                          [ ('listenerName',str),
                            ('topic',str),
                            ('eventName',str),
                            ('deliverer', DelivererRec) ])

CategoryRec = NamedTuple('CategoryRec', [
    ('categoryId', int),
    ('title', str),
    ('description', str),
    ('selected', bool)
])

CategoriesOfNotecardRec = NamedTuple('CategoriesOfNotecardRec', [
    ('notecardId', int), 
    ('categories', list[CategoryRec]),
])

NotecardRec = NamedTuple('NotecardRec', [
    ('notecardId', int|None),
    ('title', str),
    ('body', str),
    ('categories', list[CategoryRec])
])

NotecardIdTitleRec = NamedTuple('NotecardIdTitleRec', [('notecardId', int), ('title', str)])
