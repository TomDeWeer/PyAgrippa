from typing import Type, Generic, TypeVar, Optional

from PyAgrippa.AI.HashTables.HashTableEntry import HashTableEntry
from PyAgrippa.AI.HashTables.HashTableEntryInterface import HashTableEntryInterface
from PyAgrippa.Boards.Board import IBoard


E = TypeVar('E',)  # bound=HashTableEntry)  NOT NECESARRILY AN OBJECT BECAUSE MAKING OBJECT CAN BE SLOW


class HashTable(Generic[E]):
    def __init__(self, entryInterface: HashTableEntryInterface):
        self._table = {}
        self.entryInterface = entryInterface

    def __add__(self, board: IBoard, value: E):
        self._table[board.__hash__()] = value   # todo: implement replacement strategies here
        # todo: technically, one should not use the __hash__ option here if you implement the board's __eq__ method

    def __getitem__(self, board: IBoard) -> Optional[E]:
        return self._table.get(board.__hash__(), None)

    def __len__(self):
        return len(self._table)

    @classmethod
    def fromOptions(cls, **kwargs):
        return HashTable(**kwargs)

    def getEntryInterface(self):
        return self.entryInterface
