from typing import NamedTuple, Any
from collections.abc import Callable

MsgArgRec = NamedTuple('MsgArgRec',[('name', str),('value', Any)])

MsgRec = NamedTuple('MsgRec', [('topic',str),('msgName',str),('msgArgs', list[MsgArgRec])])

DelivererRec = Callable[[str, MsgRec],Any]   

ListenForRec = NamedTuple('ListenForRec',
                          [('listenerName',str),
                           ('topic',str),
                           ('msgName',str),
                           ('deliverer', DelivererRec)])

CategoryRec = NamedTuple('CategoryRec', [
    ('categoryId', int),
    ('title', str),
    ('description', str),
    ('selected', bool)
])

CategoriesOfCardRec = NamedTuple('CategoriesOfCardRec', [
    ('notecardId', int), 
    ('categories', list[CategoryRec]),
])

CardRec = NamedTuple('CardRec', [
    ('notecardId', int|None),
    ('title', str),
    ('body', str),
    ('categories', list[CategoryRec])
])

CardIdTitleRec = NamedTuple('CardIdTitleRec', 
                            [('notecardId', int),
                             ('title', str)])
